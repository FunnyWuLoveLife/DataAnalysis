#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: FunnyWu
# @license: Apache Licence
# @contact: agiot1026@163.com
# @file: qiushi_spider_by_requtests.py

import scrapy
from QiuShi_Spider.items import QiushiSpiderItem


class QiushiSpiderScrapySpider(scrapy.Spider):
    """
    QiushiSpiderScrapySpider
    糗事百科的爬虫出路逻辑
    """

    name = 'QiuShi_Spider_Scrapy'
    start_urls = [
        'https://www.qiushibaike.com',
    ]

    # start_urls = ['https://www.qiushibaike.com/8hr/page/3/?s=5000827']
    id = 0

    def parse(self, response):
        divs = response.xpath('//*[starts-with(@id,"qiushi_tag_")]')

        for div in divs:
            is_anonymity = div.xpath('.//div[@class="author clearfix"]/span')  # 用作判断是否是匿名用户

            item = QiushiSpiderItem()

            item['id'] = div.xpath(
                './/a[@class="contentHerf"]/@href').extract_first().replace('/article/', '')

            item['username'] = u'匿名用户' if is_anonymity else div.xpath(
                './/div[@class="author clearfix"]/a[2]/h2/text()').extract_first()

            item['age'] = None if is_anonymity else div.xpath(
                './/div[@class="author clearfix"]/div/text()').extract_first()

            item['sex'] = None if is_anonymity else (
                u'男' if ('manIcon' in (div.xpath('.//div[@class="author clearfix"]/div/@class').extract_first()))
                else (
                    u'女' if ('womenIcon' in (div.xpath('.//div[@class="author clearfix"]/div/@class').extract_first()))
                    else u'未知'))

            item['content_text'] = div.xpath('.//a[@class="contentHerf"]//span/text()').extract_first(),
            item['stats_vote'] = div.xpath('.//div[@class="stats"]/span[1]/i/text()').extract_first(),
            item['qiushi_comments'] = div.xpath('.//div[@class="stats"]/span[2]//i/text()').extract_first(),
            item['comment'] = {
                'cmt_name': div.xpath('.//div[@class="cmtMain"]/span[2]/text()').extract_first() if len(
                    div.xpath('./a[@class="indexGodCmt"]')) else None,
                'main_text': div.xpath('.//div[@class="cmtMain"]/div/text()').extract_first()[2:-1] if len(
                    div.xpath('./a[@class="indexGodCmt"]')) else None,
                'likenum': div.xpath('.//div[@class="cmtMain"]/div/div/text()[2]').extract_first().strip(
                    '\n') if len(div.xpath('./a[@class="indexGodCmt"]')) else None
            }

            yield item
        next_page_url = response.xpath(
            "//*[@class='pagination']//span[@class='next']/../@href").extract_first()
        if next_page_url is not None:
            if 'hot' in next_page_url:
                print u'数据爬取完成！！！'
                return
            self.parse(next_page_url)  # 递归调用
            url = response.urljoin(next_page_url)
            request = scrapy.Request(url, self.parse)
            yield request
