# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime
import requests 



dpath = "/Users/mdb/data/scrapy/aussie"
fpath = ""



class uk_flu_beta(scrapy.Spider):
    
    now =  datetime.datetime.now()
    this_year = now.year
    last_year = this_year - 1
    name = 'gamma'
    start_urls = ['http://www.health.gov.au/internet/main/publishing.nsf/Content/cda-surveil-ozflu-flucurr.htm']
    '''re patterns'''

    def parse(self,response):
        _urls = response.xpath('//*[@id="read"]/ul[6]/li/a/@href').extract()
        for item in _urls:
            #logging.log(logging.INFO, item +  ": in parse()")
            yield scrapy.http.Request(url=item, callback=self.parseAlpha)


    def parseAlpha(self,response):
        _dataConsciderations =  response.xpath('//*[@id="read"]/ul[2]/li/a/@href').extract()
        _urls = response.xpath('//*[@id="read"]/ul[3]/li/a/@href').extract()
        if _dataConsciderations:
            for item in _dataConsciderations:
                pass
        #logging.log(logging.INFO, '*****************************************************************************')
        for item in _urls:
            logging.log(logging.INFO, item +  ": in parseAlpha()")
            yield scrapy.http.Request(url=item, callback=self.parseBeta)
            #logging.log(logging.INFO, '*****************************************************************************')
            pass

    def parseBeta(self,response):
        prefix = 'http://www.health.gov.au/internet/main/publishing.nsf/'
        #_urls = response.xpath('//*[@id="read"]/ul[3]/li/a').extract()
        #_urls = response.xpath('//*[@id="read"]/ul[3]/li/a/@href').extract()
        # _urls = response.xpath('//*[@id="read"]/ul[3]/li[1]/a').extract()
        _urls = response.xpath('//*[@id="read"]/ul[3]/li/a/@href').extract()

        if(_urls):
            for item in _urls:
                #logging.log(logging.INFO, item +  ": in parseBeta()")
                _url = prefix + item
                #print _url
                self.downLoadReportAlpha(_url)
        

    def parseGamma(self,response):
        pass

    def parseDelta(self,response):
        pass

    def downLoadReportAlpha(self,_url):
        req = requests.get(_url,allow_redirects=True)
        fname = _url.split('/')[-1]
        if fname:
            req = requests.get(_url,allow_redirects=True)
            open(fname,'wb').write(req.content)




    def parse_old(self, response):
        prflag = self.if_pr()
        logging.log(logging.INFO, '*****************************************************************************')
        logging.log(logging.INFO, "Attempting to extract the AUS season report listing...........")
        logging.log(logging.INFO, '*****************************************************************************')
        #url_suffix_list = response.xpath('//*[@id="contents"]/div[1]/nav/ol/li/a/@href').extract()
        url_suffix_list = response.xpath('//*[@id="contents"]/div[2]/div/ol/li/a/@href').extract()
        sr_url_lst = list()
        if not url_suffix_list:
            logging.log(logging.INFO, '*****************************************************************************')
            logging.log(logging.INFO, "Something went left........There doesn't seem to be a listing of seasons currently provided... :-(")
            logging.log(logging.INFO, '*****************************************************************************')
            exit(-1)
        else:
            logging.log(logging.INFO, '*****************************************************************************')
            logging.log(logging.INFO, "Found seasonal reports listing...........")
            logging.log(logging.INFO, '*****************************************************************************')

            if  self.if_pr() == False:
                for suffix in url_suffix_list:
                    #sr_url_lst = self.url_prefix + suffix
                    #print "<---- seasonal reports url: " +  sr_url_lst+ " ---->"
                    print "===> " + suffix
                    yield scrapy.http.Request(url=suffix, callback=self.parse_season_reports)
            else:
                for suffix in url_suffix_list:
                    if str(self.this_year) not in suffix:
                        pass
                    else:
                        sr_url_lst = self.url_prefix + suffix
                        print "<---- seasonal reports url: " +  sr_url_lst+ " ---->"








    def parse_season_reports(self,response):
        '''
        re.search(pattern, string, flags=0)
        re.match(pattern, string, flags=0)
        re.fullmatch(pattern, string, flags=0)
        '''
        pass

    def downLoadReport(self, response):
        name = "/tmp/pdf/" + response.url.split("/")[-1]
        body = response.body
        fh = open(name, "w")
        fh.write(body )
        fh.close()



    def if_pr(self):
        return False

    def checkYear(self):
        now = datetime.datetime.now()
        current_year = now.year
        if current_year == self.cutoff_year:
            return True
        else:
            return False



