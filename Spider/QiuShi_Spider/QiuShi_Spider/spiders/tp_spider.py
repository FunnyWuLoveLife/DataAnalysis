#!/usr/bin/env python
# encoding: utf-8

# @file: tp_spider.py
# @time: 2017/7/21 11:51
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import scrapy
from QiuShi_Spider.items import TPSpiderItem


class TpSpider(scrapy.Spider):
    name = 'TPSpider'
    start_urls = [
        'http://www.thinkphp.cn/donate/index/p/1.html'
    ]

    def parse(self, response):
        lis = response.xpath("//ul[@class='donate-list']/li")
        for li in lis:
            item = TPSpiderItem()
            item['money'] = li.xpath("./span[@class='money']/text()").extract_first()
            yield item
        next_page_url = response.xpath("//div[@class='page']/a[@class='next']/@href").extract_first()
        if next_page_url is not None:
            next_page_url = 'http://www.thinkphp.cn' + next_page_url
            yield scrapy.Request(next_page_url, self.parse)
