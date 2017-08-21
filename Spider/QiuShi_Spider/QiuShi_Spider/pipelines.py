# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class QiushiSpiderPipeline(object):
    def __init__(self):
        self.count = 0
        pass

    def process_item(self, item, spider):
        if spider.name is 'QiuShi_Spider_Scrapy':
            json_item = json.dumps(dict(item), ensure_ascii=False)
            json_item_utf8 = json_item.encode(encoding='UTF-8')
            with open('./qiushi.json', 'a') as fp:
                fp.write(json_item_utf8)
                fp.write(',\n')
            print u'成功爬取第id为' + item['id'] + u'的笑话信息'
            return item
        if spider.name is 'TPSpider':
            item = dict(item)
            item['money'] = item['money'].replace(u'￥', '')
            item = float(item['money'])
            self.count += item
            json_item = json.dumps(self.count, ensure_ascii=False)
            json_item_utf8 = json_item.encode(encoding='UTF-8')
            with open('./money.txt', 'w') as fp:
                fp.write(json_item_utf8)
            return item

    def spider_closed(self, spider):
        pass
