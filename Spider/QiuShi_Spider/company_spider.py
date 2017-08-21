# !/usr/bin/env python
# encoding: utf-8

# @file: company_spider.py
# @time: 2017/7/19 14:15
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import requests
import json
import time
from pymongo import MongoClient

client = MongoClient('mongodb://FunnyWu:123456@127.0.0.1:27017/')
db_school = client.stock_spider
collection = db_school.stock


class CompanySpider:
    def __init__(self):
        pass

    def get_page_count(self, stock_type):
        url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?&stockType=' + str(stock_type) + \
              '&pageHelp.beginPage=1&pageHelp.pageSize=25&pageHelp.pageNo=1'
        response = requests.get(url, headers=self.get_request_headers(), timeout=30)
        if response.status_code is not 200:
            print '请求失败了，返回状态为：', response.status_code

        json_str = response.text
        json_obj = json.loads(json_str)
        page_count = json_obj['pageHelp']['pageCount']
        return page_count

    def run(self):

        for stock_type in range(1, 3):
            page_count = self.get_page_count(stock_type)
            for index in range(1, page_count + 1):
                url = 'http://query.sse.com.cn/security/stock/getStockListData2.do?' \
                      '&stockType=1' \
                      '&pageHelp.beginPage=' + str(index) + \
                      '&pageHelp.pageSize=25' \
                      '&pageHelp.pageNo=1'
                print '开始请求', ('A' if stock_type is 1 else 'B'), '股，第', index, '页数据'
                self.get_company_list(url)
                time.sleep(2)
        return

    def get_company_list(self, url):

        response = requests.get(url, headers=self.get_request_headers(), timeout=30)
        if response.status_code is not 200:
            print '请求失败了，返回状态为：', response.status_code

        json_str = response.text
        json_obj = json.loads(json_str)
        if json_obj['result']:
            for item in json_obj['result']:
                self.write_file(item)
        return

    def get_request_headers(self):
        '''获取request请求header'''
        headers = {
            'Host': 'query.sse.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
        }
        return headers

    def get_item(self):
        keys = {
            u'COMPANY_CODE': '',  # 公司代码
            u'COMPANY_ABBR': '',  # 公司简称
            u'SECURITY_ABBR_A': '',  # A股代码
            u'SECURITY_ABBR_B': '',  # B股代码
            u'totalShares': '',  # 总股本
            u'totalFlowShares': '',  # 流通股本
            u'': '',
        }
        return keys

    def write_file(self, item):

        for key in item.keys():
            if item[key]:
                item[key] = item[key].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        json_item = json.dumps(item, ensure_ascii=False)
        json_item_utf8 = json_item.encode(encoding='UTF-8')
        collection.insert(item)


if __name__ == '__main__':
    company_spider = CompanySpider()
    company_spider.run()
