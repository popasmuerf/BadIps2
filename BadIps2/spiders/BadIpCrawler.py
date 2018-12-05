# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
class BadipcrawlerSpider(scrapy.Spider):
    name = 'BadIpCrawler'
    #allowed_domains = ['https://www.badips.com/info/1']
    start_urls = ['http://https://www.badips.com/info/1/']
    caturl = 'https://www.badips.com/get/categories'
    rest_prefix = 'https://www.badips.com/get/info/'
    pttr_ip = '\d+\.\d+\.\d+\.\d+'
    count = 0


    def parse(self, response):
        #1. parseNames()
        #2, genCSVCol()
        #3. parseGetReport()
        #4. genReportDict()
        #5. popCSV()
        body = response.body
        self.count = self.count + 1
        iplist = re.findall(self.pttr_ip,body)
        for ip in iplist:
            rest_call = self.rest_prefix + ip
            logging.log(logging.INFO, ".....calling this REST GET method : " + rest_call)
            #yield scrapy.http.Request(url=rest_call, callback=self.retr_ipinfo)
        next_pg_lnk_list = response.xpath('//*[@id="content"]/p[2]/a/@href').extract()
        if len(next_pg_lnk_list) > 1:
            next_pg_url = next_pg_lnk_list[1]
            yield scrapy.http.Request(url=next_pg_url, callback=self.parse)
        else:
            #scrapy.http.Request(url="non_url", callback=self.dead_link)
            logging.log(logging.INFO, "{{{{{{{{{{{{{AT THE END OF THE LINE......}}}}}}}}}}}}}}}}} : ")
            reason = "SPIDER FINISHED"
            spider = self
            scrapy.signals.spider_closed(spider, reason)
            return


    def parseNames(self):
        caturl = ""
        namelst = scrapy.http.Request(url=self.caturl, callback=self.getNames)
        return namelst


    def getNames(self,response):
        body = response.body
        catdict = json.loads(body)
        namelst = catdict['Names']
        return namelst


    def gencols(self,namelst):
        collst = ['ReporterCount_sum']
        for name in namelst:
            collst.append('ReporterCount_' + 'name')
        for name in namelst:
            collst.append('Categories_' + 'name')
        for name in namelst:
            collst.append('Score_' + 'name')
        for name in namelst:
            collst.append('LastReport_' + 'name')
        return collst