# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from pymongo import MongoClient


class ZhihuSpiderPipeline(object):
    def __init__(self):
        self.client = MongoClient('mongodb://funnywu:funnywu1026@101.200.54.171/', 27017)
        user_info = self.client.zhihu_spider
        self.user = user_info.user
        pass

    def process_item(self, item, spider):
        item = dict(item)
        # json_item = json.dumps(dict(item), ensure_ascii=False)
        # json_item_utf8 = json_item.encode(encoding='UTF-8')
        self.user.insert(item)
        return item

    def spider_closed(self, spider):
        self.client.close()
        pass
