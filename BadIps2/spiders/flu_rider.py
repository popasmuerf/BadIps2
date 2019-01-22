# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime



class flu_rider(scrapy.Spider):
    '''global configurations'''
    urlPrefix = 'https://www.gov.uk'
    reportUrlPrefix = 'https://assets.publishing.service.gov.uk'
    now =  datetime.datetime.now()
    thisYear = now.year
    lastYear = thisYear - 1
    thisYearStr = str(thisYear)
    lastYearStr = str(lastYear)
    prevRunFlag = False

    name = 'rider'
    start_urls = ['https://www.gov.uk/government/collections/weekly-national-flu-reports']

    '''re patterns'''
    full_url_pttrn = 'http(s){0,1}://(\w+\.){1,10}\w+(\/\w+){1,10}\.(pdf|ods|xls|xlsx|xlsm|doc|docx|docm|sxw|stw|doc|xml)'
    part_url_pattrn = '(\/\w+){1,10}.pdf'






    def parse(self,response):
        nextUrlList = []
        suffixList = response.xpath('//*[@id="contents"]/div[2]/div/ol/li/a/@href').extract()
        thisYearSeasonalReportUrl  = ''
        for s in suffixList:
            s = s.strip()
            nextUrlList.append(self.urlPrefix + s)
            result = re.findall(self.lastYearStr+'-to-'+self.thisYearStr+'-season',s)
            if result:
                thisYearSeasonalReportUrl = self.urlPrefix + s
        if not nextUrlList:
            #log
            exit()
        else:
            if self.prevRunFlag:
                yield scrapy.Request(url=thisYearSeasonalReportUrl, callback=self.parseSeasonalReports)
            else:
                for _url in nextUrlList:
                    yield scrapy.Request(url=_url, callback=self.parseAllSeasonalReports)


    def getMoth(self):
        #create month map
        #create

    def parsSeasonalReports(self,response):
        #get link to weekly reports
        #follow weekly reports path
        pass

    def parseWeeklyReports(selfs,response):
        #get the current month
        #get list of reports for that month
        #download these reports
        pass

    def parseAllSeasonalReports(self,response):
        '''Some of these urls embedded into the html are only partial...we need to check
           for this and and complete the url where ever we find them.....'''
        urLst  = response.xpath('//*/div[2]/h2/a/@href').extract()
        for _url in urLst:
            result = re.findall('https{0,1}://',_url)
            if result:
                print _url

            else:
                _url = self.reportUrlPrefix + _url
                print _url
        pass


    def parseWeeklyReports(self,response):
        pass




    def downloadReport(self):
        pass