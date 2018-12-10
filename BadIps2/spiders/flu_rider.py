# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime



class flu_rider(scrapy.Spider):
    name = 'flu'
    #allowed_domains = ['https://www.badips.com/info/1']
    start_urls = ['https://www.gov.uk/government/statistics/weekly-national-flu-reports-2018-to-2019-season']

    #now = datetime.datetime.now()
    #year = now.year

    def parse(self, response):
        reportUrlLinksLst = response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a/@href').extract()
        for rurlLst in reportUrlLinksLst:
            _url = rurlLst.strip('')
            #self.downloadLoadReports(_url)
            yield scrapy.Request(url=_url, callback=self.parseII)


    def parseII(self,response):
        pdflst = response.xpath('//*/div[2]/h2/a/@href').extract()
        for _url in pdflst:
            if _url.__contains__('https'):
                yield scrapy.Request(url=_url,callback=self.downLoadReport)



    def downLoadReport(self, response):
        name = "/tmp/" + response.url.split("/")[-1]
        body = response.body
        fh = open(name, "w")
        fh.write(body )
        fh.close()
