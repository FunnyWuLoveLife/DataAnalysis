# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()  # 个人URL
    profile_name = scrapy.Field()  # 昵称
    location = scrapy.Field()  # 居住地
    profession = scrapy.Field()  # 所处行业
    work = scrapy.Field()  # 职业经历,数组
    resume = scrapy.Field()  # 个人简介
    one_sentence_introduction = scrapy.Field()  # 一句话简介
    gender = scrapy.Field()  # 性别
    education = scrapy.Field()  # 教育经历,数组
    followers = scrapy.Field()  # 关注他的人
    followers_quantity = scrapy.Field()  # 关注他的人
    following = scrapy.Field()  # 他关注的人
    following_quantity = scrapy.Field()  # 他关注的人
    favour = scrapy.Field()  # 获得赞同次数
    thank = scrapy.Field()  # 获得感谢数量
    collection = scrapy.Field()  # 获得收藏数量
