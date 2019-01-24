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
    monthLst = ["null_month"
                 "january",
                 "February",
                 "March",
                 "April",
                 "May",
                 "June",
                 "July",
                 "August",
                 "September",
                 "October",
                 "November",
                 "December",]
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


    def getMonth(self):
        #create month map
        #create
        pass

    def parsSeasonalReports(self,response):
        #get link to weekly reports
        #follow weekly reports path
        urllist = response.xpath('//*[@id="content"]/div[3]/div[2]/div/div/nav/ul/li[1]/a/@href').extract()
        #check if urlist is empty
        if not urllist:
            exit(-1)
        else:
            _url = urllist[1]
            result = re.findall('https{0,1}://',_url)
            if result:
                _url = 'https://www.gov.uk/government/collections/weekly-national-flu-reports'
                #call parseWeeklyReports
                pass
            else:
                _url =  'https://www.gov.uk' + _url
                #call parseWeeklyReports
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



def parseWeeklyReports(self,response):
    urllist = response.xpath('//*[@id="contents"]/div[2]/div/ol/li/a/@href').extract()
    if not urllist:
        exit(-1)
    else:
        for _url in urllist:
            if _url.find(self.thisYearStr) == -1:
                pass
            else:
                result = re.findall('https{0,1}://',_url)
                if result:
                    #follw path and download all files
                    pass
                else:
                    _url = self.reportUrlPrefix + _url
                    #follow path and download all files







def downloadAllReports(self,response):
    monthInt = self.now.month
    monthStr = self.monthLst[monthInt]

    pass