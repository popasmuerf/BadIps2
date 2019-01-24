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

    prevRunFlag = True


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
            exit()
        else:
            if self.prevRunFlag:
                weeklyReportUrl = 'https://www.gov.uk/government/collections/weekly-national-flu-reports'
                yield scrapy.Request(url=weeklyReportUrl, callback=self.getWeeklyList)
            else:
                for _url in nextUrlList:
                    yield scrapy.Request(url=_url, callback=self.parseAllSeasonalReports)


    def getWeeklyList(self,response):
        urllist = response.xpath('//*[@id="contents"]/div[2]/div/ol/li/a/@href').extract()
        substr = 'weekly-national-flu-reports-' + self.lastYearStr + '-to-'+ 'self.thisYearStr' + '-season'
        for _url in urllist:
            foundThisYearFlag = _url.find(substr)!= -1
            result = re.findall('https{0,1}://',_url)
            if foundThisYearFlag and result:
                yield scrapy.Request(url=_url,callback=self.downloadWeeklyReport)
            else:
                _url =  self.urlPrefix + _url
                yield scrapy.Request(url=_url,callback=self.downloadWeeklyReport)






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




    def downloadWeeklyReport(self,response):
        from datetime import date
        weekNum = date.today().isocalendar()[1]
        weekNumStr = str(weekNum)
        urllist = response.xpath('//*/div[2]/h2/a/@href').extract()

        for _url in urllist:
            yearFlag = _url.find(self.thisYearStr) != -1
            weekFlag =  _url.find('week_' + weekNumStr + '_' + self.thisYearStr) != -1

            if weekFlag and yearFlag:
                result = re.findall('https{0,1}://',_url)
                if result:
                    print _url
                else:
                    urlComplete = self.urlPrefix + _url
                    #print urlComplete
