# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:57:59 2017

@author: George
"""

#import urlparse
import scrapy

from scrapy.http import Request

class lcrmscp(scrapy.Spider):
    name = "lcrmscp"

    allowed_domains = ["www.lcrmscp.gov"]
    start_urls = ["https://www.lcrmscp.gov/steer_committee/technical_reports.html"]

    def parse(self, response):
        for href in response.css('div#all_results h3 a::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.parse_article
            )

    def parse_article(self, response):
        for href in response.css('div.download_wrapper a[href$=".pdf"]::attr(href)').extract():
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pdf
            )

    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)