# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime



class flu_rider(scrapy.Spider):
    cutoff_year = 2020
    name = 'uk_flu'
    start_urls = ['https://www.gov.uk/government/collections/weekly-national-flu-reports']

    def parse(self, response):
        reportUrlLinksLst = response.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/div[2]/div/div/ul/li/a/@href').extract()
        for rurlLst in reportUrlLinksLst:
            _url = rurlLst.strip('')
            if self.checkYear():
                yield scrapy.Request(url=_url, callback=self.parseII)
            else:
                now = datetime.datetime.now()
                current_year = now.year
                if _url.__contains__(current_year):
                    yield scrapy.Request(url=_url, callback=self.parseII)


    def parseII(self,response):
        pdflst = response.xpath('//*/div[2]/h2/a/@href').extract()
        for _url in pdflst:
            if _url.__contains__('https'):
                yield scrapy.Request(url=_url,callback=self.downLoadReport)
            else:
                _url = 'https://www.gov.uk' + _url
                yield scrapy.Request(url=_url,callback=self.downLoadReport)



    def downLoadReport(self, response):
        name = "/tmp/pdf/" + response.url.split("/")[-1]
        body = response.body
        fh = open(name, "w")
        fh.write(body )
        fh.close()



    def checkYear(self):
        now = datetime.datetime.now()
        current_year = now.year
        if current_year == self.cutoff_year:
            return True
        else:
            return False



