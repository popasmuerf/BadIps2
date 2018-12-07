# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
class flu_rider(scrapy.Spider):
    name = 'flu'
    #allowed_domains = ['https://www.badips.com/info/1']
    start_urls = ['https://www.badips.com/info/1/']
    caturl = 'https://www.badips.com/get/categories'
    rest_prefix = 'https://www.badips.com/get/info/'
    pttr_ip = '\d+\.\d+\.\d+\.\d+'
    count = 0
    __file__ = "db.txt"
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    __fpath__ = __location__ + "/" + __file__
    clist = []


    def parse(self, response):
        body = response.body
