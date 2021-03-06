# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime



class uk_flu_alpha(scrapy.Spider):
    url_prefix = 'https://www.gov.uk'
    report_url_prefix = 'https://assets.publishing.service.gov.uk'
    now =  datetime.datetime.now()
    this_year = now.year
    last_year = this_year - 1
    name = 'alpha'
    start_urls = ['https://www.gov.uk/government/collections/weekly-national-flu-reports']
    '''re patterns'''

    full_url_pttrn = 'http(s){0,1}://(\w+\.){1,10}\w+(\/\w+){1,10}\.(pdf|ods|xls|xlsx|xlsm|doc|docx|docm|sxw|stw|doc|xml)'

    part_url_pattrn = '(\/\w+){1,10}.pdf'






    def parse(self, response):
        prflag = self.if_pr()
        logging.log(logging.INFO, '*****************************************************************************')
        logging.log(logging.INFO, "Attempting to extract the season report listing...........")
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



