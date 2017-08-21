# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhaopinItem(scrapy.Item):
    # define the fields for your item here like:
    area = scrapy.Field()  # 区域
    detail_url = scrapy.Field()  # 详情页url
    position_name = scrapy.Field()  # 职位名称
    position_intro = scrapy.Field()  # 职位简介
    position_category = scrapy.Field()  # 职位类型
    salary = scrapy.Field()  # 薪水
    update_tiem = scrapy.Field()  # 更新时间
    experience = scrapy.Field()  # 工作经验
    hiring_number = scrapy.Field()  # 招聘人数
    degree = scrapy.Field()  # 学历
    work_address = scrapy.Field()  # 工作地址
    welfare = scrapy.Field()  # 福利
    phone = scrapy.Field()  # 电话
    contacts = scrapy.Field()  # 联系人
    company_name = scrapy.Field()  # 公司名称
    company_scal = scrapy.Field()  # 公司规模
    company_property = scrapy.Field()  # 公司性质
    company_profession = scrapy.Field()  # 所属行业
    company_address = scrapy.Field()  # 公司地址
    company_intro = scrapy.Field()  # 公司简介
