# -*- coding: utf-8 -*-
"""
Crawl the XBRL files from monthly RSS feed
    http://www.sec.gov/Archives/edgar/monthly/xbrlrss-{year}-{month}.xml

Output:
    - xbrl.zip files stored under <year>/<month> directory

Output structure:
|-- 2018
|-- 2017
    |-- <12>
        |-- <cik>-<...>-xbrl.zip
|-- 2016
|-- 2015
 .
 .
 .
|-- 2005

On subsequent crawls, only the new or updated XBRL files will be stored.

Usage:
    crawlee -n run SecEdgarRss crawl [year [month] | from_year to_year] [index_only=true]

    # crawl only the current month
    crawlee -n run SecEdgarRss crawl

    # crawl Sep 2017
    crawlee -n run SecEdgarRss crawl month=9 year=2017

    # crawl year 2015
    crawlee -n run SecEdgarRss crawl year=2015

    # crawl year 2010, Jan to Mar
    crawlee -n run SecEdgarRss crawl year=2010 from_month=1 to_month=3

    # crawl from 2010-2014
    crawlee -n run SecEdgarRss crawl from_year=2010 to_year=2014

    # crawl everything
    crawlee -n run SecEdgarRss crawl first_run=true

    Note: `index_only=true` will only crawl the RSS feed but not the XBRL files

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from builtins import *

from datetime import datetime

import xml.etree.ElementTree as ET
import feedparser

from crawleeapi.core import extract, parsers, smac_context, spiders, swob

# Earliest year with available data
YEAR_MIN = 2005


class SpiderModeCrawl(spiders.CrawleeSpiderMode):

    def modify_start_urls(self, start_urls, smac):
        """Modify the `start_urls` based on the values of the spider attributes.

        Available custom spider attributes are:
            year (int): The year to crawl, from `YEAR_MIN` to current year.
            month (int): The month to crawl, from 1 to 12.
            from_year (int): For a range of years to crawl, this is the starting year.
            to_year (int): For a range of years to crawl, this is the ending year.

        Args:
            start_urls (list): By default, is a copy of `START_URLS`.
            smac: A reference to current spider context.

        Returns:
            start_urls (list of tuples): Contains a list of ``(url, meta)``
                Each `url` corresponds to the RSS feed for a given year and month.
                The `meta` is a ``dict`` containing `year` and `month`.
        """
        base_url = start_urls[0]
        start_urls = []

        months = range(1, 12 + 1)
        now = datetime.utcnow()

        # Crawl given `year`
        if smac.attrs.get('year', 0):
            from_year = to_year = smac.attrs.year

            # Crawl only the specified `month`
            if smac.attrs.get('month', 0) and smac.attrs.month in range(1, 12+1):
                months = [smac.attrs.month]

            # Crawl the range of months
            elif smac.attrs.get('from_month', 0) and smac.attrs.get('to_month', 0):
                months = list(range(smac.attrs.from_month, smac.attrs.to_month+1))

            # Crawl only from the months of Jan to current month
            elif smac.attrs.year == now.year:
                months = range(1, now.month + 1)

        # Crawl the given range of years
        elif smac.attrs.get('from_year', 0) and smac.attrs.get('to_year', 0):
            from_year = smac.attrs.from_year
            to_year = smac.attrs.to_year

        else:
            to_year = now.year

            # Crawl from `YEAR_MIN` to current year-month, on first run
            if smac.meta.first_run:
                from_year = YEAR_MIN

            # Crawl only the current month
            else:
                from_year = now.year
                months = [now.month]

        # Create a list of ``(year, month)``, in descending order
        dates = []
        if from_year < to_year:
            for y in range(to_year, from_year-1, -1):
                if YEAR_MIN <= y <= now.year:
                    # ensure future months are excluded
                    _months = range(1, now.month + 1) if y == now.year else months

                    for m in reversed(_months):
                        dates.append((y, m))
        elif from_year == to_year:
            if YEAR_MIN <= from_year <= now.year:
                for m in reversed(months):
                    dates.append((from_year, m))

        if len(dates) > 1:
            self.log.info('Current crawl will process months from {}-{} to {}-{}.'.format(
                dates[0][0], dates[0][1], dates[-1][0], dates[-1][1]
            ))
        elif len(dates) == 1:
            self.log.info('Current crawl will process month {}-{}.'.format(*dates[0]))
        else:
            self.log.error('No month to process; invalid user input(s).')

        for ym in dates:
            meta = dict(year=ym[0], month=str(ym[1]).zfill(2))
            url = base_url.format(**meta)
            self.log.info(url)
            start_urls.append((url, meta))
        return start_urls

    def parse(self, response):
        """Process the RSS feed for a given month.

        We have to unfortunately use both feedparser (for normal cases) and
        ET for old-style RSS feeds because feedparser cannot handle the case
        where multiple xbrlFiles are referenced without enclosure.

        Args:
            response: Contains the downloaded XML for the RSS.

        Yields:
            SWOBRequest: The request that corresponds to each XBRL item.

        """
        smac = smac_context.get_from(response)
        max_items = smac.attrs['max_items']
        stats_year = '{}/{}/{}'.format(self.spider.name,
                                       response.request.meta['year'],
                                       '{info}')
        stats_month = '{}/{}/{}/{}'.format(self.spider.name,
                                           response.request.meta['year'],
                                           response.request.meta['month'],
                                           '{info}')

        self.log.debug(response.url)
        item_index = -1
        filedir = '{}/{}'.format(response.request.meta['year'], response.request.meta['month'])

        try:
            root = ET.fromstring(response.body)
        except ET.ParseError as perr:
            self.log.error('XML Parser Error:', perr)
        feed = feedparser.parse(response.body)
        try:
            self.log.info(feed['channel']['title'])
        except KeyError as e:
            self.log.error('Key Error:', e)

        # Process RSS feed and walk through all items contained
        for item in feed.entries:
            item_index += 1
            try:
                cik = item['edgar_ciknumber']
                form_type = item['edgar_formtype']
                if form_type not in ['10-K', '10-K/A', '10-KT', '10-KT/A']:
                    smac.stats.inc_value(stats_year.format(info='excluded/{}'.format(form_type)))
                    smac.stats.inc_value(stats_year.format(info='excluded/TOTAL'))
                    continue
                else:
                    smac.stats.inc_value(stats_year.format(info='item/TOTAL'))
                    smac.stats.inc_value(stats_month.format(info='item/TOTAL'))

                # Identify zip file enclosure, if available
                enclosures = [l for l in item['links'] if l['rel'] == 'enclosure']

                # Zip file enclosure exists, so we can just download the zip file
                if len(enclosures):
                    smac.stats.inc_value(stats_year.format(info='item/with_enclosure'))
                    smac.stats.inc_value(stats_month.format(info='item/with_enclosure'))
                    if smac.attrs.getbool('index_only'):
                        continue

                    url = enclosures[0]['href']

                    yield swob.SWOBRequest(
                        url=url,
                        filedir=filedir,
                        filename=cik+'-{{ req.utfp.filename }}',
                        follow_on_score=swob.FOLLOW_IF_NEW_OR_IF_UNSAVED,
                        callback=self.download_file
                    )

                # Create a request to download the individual files and create a zip
                else:
                    smac.stats.inc_value(stats_year.format(info='item/without_enclosure'))
                    smac.stats.inc_value(stats_month.format(info='item/without_enclosure'))
                    if smac.attrs.getbool('index_only'):
                        continue

                    edgar_namespace = {'edgar': 'http://www.sec.gov/Archives/edgar'}
                    current_item = list(root.iter('item'))[item_index]
                    xbrl_filing = current_item.find('edgar:xbrlFiling', edgar_namespace)
                    xbrl_files_item = xbrl_filing.find('edgar:xbrlFiles', edgar_namespace)
                    xbrl_files = xbrl_files_item.findall('edgar:xbrlFile', edgar_namespace)

                    # The urls of the files that will be downloaded and stored in a zip
                    file_urls = []
                    for xf in xbrl_files:
                        xf_url = xf.get('{http://www.sec.gov/Archives/edgar}url')
                        if xf_url.endswith(('.xml', '.xsd')):
                            file_urls.append(xf_url)
                            self.log.debug('------', xf_url)

                    url = item['link']
                    yield swob.SWOBRequest(
                        url=url,
                        filedir=filedir,
                        filename=cik+'-{{ req.utfp.filestring }}-xbrl.zip',
                        follow_on_score=swob.FOLLOW_IF_NEW_OR_IF_UNSAVED,
                        callback=self.download_zip_file_set,
                        http_full_response='do not download; response not important',

                        # The `download_zip_file_set` callback requires the `file_urls`
                        metadata=dict(file_urls=file_urls)
                    )

            except Exception:
                smac.stats.inc_value(stats_year.format(info='item_with_error'))
                self.log.error('Error with item_index={}'.format(item_index), exc_info=True)

            if smac.meta.dry_run or (item_index >= max_items):
                # Stop the crawl
                break


class Spider(spiders.CrawleeSpider):
    name = 'SecEdgarRss'
    group = 'cyber-insurance'
    modes = spiders.CrawleeSpiderModes([
        ('crawl', SpiderModeCrawl),
    ])

    ref = 'EXTR-433'
    tags = ['done']
    changelog = [
        ('2018.04.15', 'micmejia', 'add from_month and to_month crawl custom parameters'),
        ('2018.04.09', 'micmejia', 'filter the items to crawl based on form_type'),
        ('2018.04.03', 'micmejia', 'update code for downloading items without enclosure'),
        ('2018.03.27', 'micmejia', 'initial version'),
    ]

    crawlee_version_min = '1.10.6'
    custom_attrs = dict(month=int, year=int, from_year=int, to_year=int,
                        from_month=int, to_month=int, index_only=bool)
    custom_settings = spiders.CrawleeSpider.merge_custom_settings(dict(
        START_URLS=['https://www.sec.gov/Archives/edgar/monthly/xbrlrss-{year}-{month}.xml'],
        SWOB_ALL_REQUEST_DEFAULTS=dict(metadata_captured=True),
        AUTOTHROTTLE_MAX_DELAY=5,
        DOWNLOAD_DELAY=0.1,
        TELNETCONSOLE_ENABLED=True
    ))