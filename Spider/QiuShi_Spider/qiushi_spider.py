#!/usr/bin/env python
# encoding: utf-8

# @file: qiushi_spider.py
# @time: 2017/7/18 16:01
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm

import requests
from scrapy import Selector
import json
import time

BASE_URL = "https://www.qiushibaike.com"

ROOT_RULE = '//div[@id="content-left"]/div'

RULE = {
    'id': './a[@class="contentHerf"]/@href',
    'username': './div[@class="author clearfix"]/a[2]/h2/text()',
    'age': './div[@class="author clearfix"]/div/text()',
    'sex': './div[@class="author clearfix"]/div/@class',
    'content-text': 'string(./a[@class="contentHerf"])',
    'stats-vote': './div[@class="stats"]/span[2]//i/text()',
    'qiushi_comments': './div[@class="stats"]/span[2]//i/text()',
    'cmt-name': './/div[@class="cmtMain"]/span[2]/text()',
    'main-text': './/div[@class="cmtMain"]/div/text()',
    'likenum': './/div[@class="cmtMain"]/div/div/text()[2]'
}


class QiuShi:
    def __init__(self):
        pass

    def get_joke_list(self, url):
        '''获取单页面中的笑话列表'''
        herders = {
            'Host': 'www.qiushibaike.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        }
        response = requests.get(url, headers=herders, verify=False)

        if response.status_code is not 200:
            print u'请求出错了，错误代码:', response.status_code
            return

        body = Selector(text=response.text)
        divs = body.xpath(ROOT_RULE)
        for div in divs:
            is_anonymity = div.xpath('./div[@class="author clearfix"]/span')  # 用作判断是否是匿名用户
            item = {
                'id': div.xpath(RULE['id']).extract_first().replace('/article/', ''),
                'username': u'匿名用户' if is_anonymity else div.xpath(RULE['username']).extract_first(),
                'age': '' if is_anonymity else div.xpath(RULE['age']).extract_first(),
                'sex': '' if is_anonymity else
                (u'男' if ('manIcon' in (div.xpath(RULE['sex']).extract_first()))
                 else (u'女' if ('womenIcon' in (div.xpath(RULE['sex']).extract_first()))
                       else u'未知')),

                'content-text': div.xpath(RULE['content-text']).extract_first().strip('\n'),
                'stats-vote': div.xpath(RULE['stats-vote']).extract_first(),
                'qiushi_comments': div.xpath(RULE['qiushi_comments']).extract_first(),

                'cmt-name': div.xpath(RULE['cmt-name']).extract_first() if len(
                    div.xpath('./a[@class="indexGodCmt"]')) else '',

                'main-text': div.xpath(RULE['main-text']).extract_first()[2:-1]
                if len(div.xpath('./a[@class="indexGodCmt"]'))
                else '',

                'likenum': div.xpath(RULE['likenum']).extract_first().strip('\n')
                if len(div.xpath('./a[@class="indexGodCmt"]'))
                else '',
            }
            self.write_file(item)

        # 通过函数递归，获取下一页列表
        time.sleep(1)
        next_page_url = self.get_next_page_url(body_selector=body)
        if 'hot' in next_page_url:
            print '数据爬取完成！！！'
            return
        self.get_joke_list(next_page_url)  # 递归调用
        return

    def get_next_page_url(self, body_selector):
        '''获取当前给定的selector中的下一页url'''
        next_page_url = body_selector.xpath("//*[@class='pagination']//span[@class='next']/../@href").extract_first()
        return BASE_URL + next_page_url

    def write_file(self, item):
        json_item = json.dumps(item, ensure_ascii=False)
        json_item_utf8 = json_item.encode(encoding='UTF-8')
        with open('./qiushi.json', 'a') as fp:
            fp.write(json_item_utf8)
            fp.write(',\n')
        print u'成功爬取第id为' + item['id'] + u'的笑话信息'

    def run(self):
        '''爬虫程序入口'''
        self.get_joke_list(BASE_URL)


if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.run()
