# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import json
import re


class ZhaopinPipeline(object):
    def __init__(self):
        self.client = MongoClient('mongodb://FunnyWu:123456@127.0.0.1:27017/')
        db_school = self.client.jobs_spider

        self.db_zhaopin = db_school.zhaopin
        # self.fp = open('./zhaopin.json', 'w')

    def process_item(self, item, spider):
        item = dict(item)
        for key in item.keys():
            if item[key]:
                item[key] = item[key].replace('\n', '').replace('\t', '').replace('\r', '').strip(' ')
        self.db_zhaopin.insert(item)
        # json_item = json.dumps(item, ensure_ascii=False)
        # json_item_utf8 = json_item.encode(encoding='UTF-8')
        # self.fp.write(json_item_utf8)
        return item

    def spider_closed(self, spider):
        self.client.close()
        # self.fp.close()
        pass
