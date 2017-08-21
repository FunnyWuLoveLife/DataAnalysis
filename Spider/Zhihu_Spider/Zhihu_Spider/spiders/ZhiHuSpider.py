#!/usr/bin/env python
# encoding: utf-8

# @file: ZhiHuSpider.py
# @time: 2017/7/30 21:48
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import scrapy
from Zhihu_Spider.items import ZhihuSpiderItem
import re


class ZhiHuSpider(scrapy.Spider):
    BASE_URL = 'https://www.zhihu.com'
    name = 'ZhiHuSpider'
    start_urls = [
        'https://www.zhihu.com/people/jin-hai-tao-96-83'
    ]

    def parse(self, response):
        item = ZhihuSpiderItem()
        item['url'] = response.url
        item['profile_name'] = response.xpath("//span[@class='ProfileHeader-name']/text()").extract_first()
        info_items = response.xpath("//div[@class='ProfileHeader-info']/div[@class='ProfileHeader-infoItem']")

        for info in info_items:
            svg_class = info.xpath("./div[@class='ProfileHeader-iconWrapper']/svg/@class").extract_first()
            if 'female' in svg_class:
                item['gender'] = 'male'
            elif 'male' in svg_class:
                item['gender'] = 'female'
        item['following_quantity'] = response.xpath(
            "//div[@class='NumberBoard FollowshipCard-counts']/a[1]/div[2]/text()").extract_first()
        item['followers_quantity'] = response.xpath(
            "//div[@class='NumberBoard FollowshipCard-counts']/a[2]/div[2]/text()").extract_first()
        thank_favour = response.xpath("//div[@class='Profile-sideColumnItemValue']/text()").extract_first()
        if thank_favour:
            thank_favour = re.findall(r"\d+\.?\d*", thank_favour)
            if thank_favour:
                item['thank'] = thank_favour[0]
                item['favour'] = thank_favour[1]

        following_url = response.xpath("//a[@class='Button NumberBoard-item Button--plain'][1]/@href").extract_first()
        following_url = self.BASE_URL + following_url
        yield scrapy.Request(following_url, self.get_following, headers=self.get_headers(response.url),
                             meta={'item': item})

    def get_following(self, response):
        item = response.meta['item']

        following_divs = response.xpath("//div[@id='Profile-following']/div[2]/div")
        for following in following_divs:
            people_url = following.xpath(
                "./div/div/div[@class='ContentItem-head']//h2/div/span/div/div/a/@href") \
                .extract_first()
            if people_url:
                people_url = self.BASE_URL + people_url
                if '/people/' in people_url:
                    yield scrapy.Request(people_url, self.parse)

        followers_url = response.xpath("//a[@class='Button NumberBoard-item Button--plain'][2]/@href").extract_first()
        followers_url = self.BASE_URL + followers_url
        yield scrapy.Request(followers_url, self.get_followers, headers=self.get_headers(response.url),
                             meta={'item': item})

    def get_followers(self, response):
        item = response.meta['item']
        yield item

    def get_headers(self, referer_url):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'www.zhihu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': referer_url,
        }
        return headers
