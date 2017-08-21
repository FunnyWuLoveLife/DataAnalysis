# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiushiSpiderItem(scrapy.Item):
    id = scrapy.Field()
    username = scrapy.Field()
    age = scrapy.Field()
    sex = scrapy.Field()
    content_text = scrapy.Field()
    stats_vote = scrapy.Field()
    qiushi_comments = scrapy.Field()
    comment = scrapy.Field()


class TPSpiderItem(scrapy.Item):
    money = scrapy.Field()
