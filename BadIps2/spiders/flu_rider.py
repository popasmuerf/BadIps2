# -*- coding: utf-8 -*-
import scrapy
import json
import logging
import re
import os
import datetime



class flu_rider(scrapy.Spider):
    name = "red"
    start_urls = ["freebsd.org"]
    def parse(selfs,body):
        pass