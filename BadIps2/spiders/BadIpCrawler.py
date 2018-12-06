# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
class BadipcrawlerSpider(scrapy.Spider):
    name = 'bi'
    #allowed_domains = ['https://www.badips.com/info/1']
    start_urls = ['https://www.badips.com/info/1/']
    caturl = 'https://www.badips.com/get/categories'
    rest_prefix = 'https://www.badips.com/get/info/'
    pttr_ip = '\d+\.\d+\.\d+\.\d+'
    count = 0
    __file__ = "categories.txt"
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __fpath__ = __location__ + "/" + __file__
    clist = []


    def parse(self, response):
        #1. parseNames()
        #2, genCSVCol()
        #3. parseGetReport()
        #4. genReportDict()
        #5. popCSV()
        catNameLst = self.getCatNames()
        logging.log(logging.INFO, str(catNameLst))
        catColsLst = self.genCols(catNameLst)
        logging.log(logging.INFO, str(catColsLst))

        '''
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
            #logging.log(logging.INFO, ".....calling this REST GET method : " + next_pg_url)
            yield scrapy.http.Request(url=next_pg_url, callback=self.parse)

        else:
            #scrapy.http.Request(url="non_url", callback=self.dead_link)
            logging.log(logging.INFO, "{{{{{{{{{{{{{AT THE END OF THE LINE......}}}}}}}}}}}}}}}}} : ")
            reason = "SPIDER FINISHED"
            spider = self
            scrapy.signals.spider_closed(spider, reason)
            return
            '''


    def getCatNames(self):
        namelst = ['ssh',
                   'postfix',
                   'dovecot-pop3imap',
                   'apache',
                   'apache-defensible',
                   'apache-404',
                   'apache-noscript',
                   'apache-nohome',
                   'apache-overflows',
                   'apache-scriddies',
                   'apacheddos',
                   'apache-php-url-fopen',
                   'apache-spamtrap',
                   'phpids',
                   'Php-url-fopen',
                   'rfi-attack',
                   'sql',
                   'sql-injection',
                   'sql-attack',
                   'ddos',
                   'qmail-smtp',
                   'screensharingd',
                   'ftp',
                   'dovecot-pop3',
                   'exim',
                   'sshd',
                   'pop3',
                   'imap',
                   'sip',
                   'sasl',
                   'courierpop3',
                   'ssh-ddos']
        return namelst



    def genCols(self,catNameLst):
        collst = ['ReporterCount_sum']
        for name in catNameLst:
            collst.append('ReporterCount_' + name)
        for name in catNameLst:
            collst.append('Categories_' + name)
        for name in catNameLst:
            collst.append('Score_' + name)
        for name in catNameLst:
            collst.append('LastReport_' + name)
        collst.append('Whois')
        collst.append('Ports')
        collst.append('CountryCode')
        collst.append('rDNS')
        collst.append('suc')
        collst.append('IP')
        collst.append('Listed')

        return collst


'''
    def parseNames(self):
        caturl = ""
        namelst = scrapy.http.Request(url=self.caturl, callback=self.getNames)
        return namelst


    def getNames(self,response):
        body = response.body
        catdict = json.loads(body)
        namelst = catdict['Names']
        return namelst

    def getName2(self):
        __file__ = "categories.txt"
        logging.log(logging.INFO, "__file__ = " + self.__file__)
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        logging.log(logging.INFO, "__location__ = " + self.__location__)
        __fpath__ = __location__ + "/" + __file__
        logging.log(logging.INFO, "____fpath____ = " + self.__fpath__)

        with open(self.__fpath__) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            #print content
            logging.log(logging.INFO, content)
            self.clist = content
            f.close() 
'''