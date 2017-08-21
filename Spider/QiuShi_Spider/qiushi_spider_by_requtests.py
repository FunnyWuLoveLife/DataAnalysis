#!/usr/bin/env python
# encoding: utf-8

# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @file: qiushi_spider_by_requtests.py
# @time: 2017/7/14 15:43

import requests
from lxml import etree
import pandas as pd
from scrapy import Selector
import json
import time

BASE_URL = "https://www.qiushibaike.com"

ROOT_RULE = '//div[starts-with(@id,"qiushi_tag_")]'

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

joke_list = []


class QiuShiSpiderRequest(object):
    count = 1

    def __init__(self):
        pass

    @staticmethod
    def get_source(url):

        herders = {
            "Host": "www.qiushibaike.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
        response = requests.get(url, herders=herders)
        response.content
        return response.text

    def get_joke_info(self, source_html):
        """
        :param source_html: 请求得到的页面
        :return: 一个存储着笑话的list
        """
        body_selector = Selector(text=source_html)
        divs = body_selector.xpath(ROOT_RULE)
        for key in divs:
            is_anonymity = key.xpath('.//div[@class="author clearfix"]/span')  # 用作判断是否是匿名用户
            item = {
                'id': key.xpath(RULE['id']).extract_first().replace('/article/', ''),
                'username': '匿名用户' if is_anonymity else key.xpath(RULE['username']).extract_first(),
                'age': '' if is_anonymity else key.xpath(RULE['age']).extract_first(),
                'sex': '' if is_anonymity else
                ('男' if ('manIcon' in (key.xpath(RULE['sex']).extract_first()))
                 else ('女' if ('womenIcon' in (key.xpath(RULE['sex']).extract_first()))
                       else '未知')),

                'content-text': key.xpath(RULE['content-text']).extract_first().strip('\n'),
                'stats-vote': key.xpath(RULE['stats-vote']).extract_first(),
                'qiushi_comments': key.xpath(RULE['qiushi_comments']).extract_first(),

                'cmt-name': key.xpath(RULE['cmt-name']).extract_first() if len(
                    key.xpath('./a[@class="indexGodCmt"]')) else '',

                'main-text': key.xpath(RULE['main-text']).extract_first()[2:-1]
                if len(key.xpath('./a[@class="indexGodCmt"]'))
                else '',

                'likenum': key.xpath(RULE['likenum']).extract_first().strip('\n')
                if len(key.xpath('./a[@class="indexGodCmt"]'))
                else '',
            }

            self.save_item(item)
            print u'成功爬取第' + str(self.count) + u'条，id为' + item['id'] + u'的笑话信息'
            self.count += 1

        next_url = self.get_next_page_url(source_html)
        if 'hot' in next_url or None:
            return
        # time.sleep(1)
        netx_page_source = self.get_source(BASE_URL + next_url)
        self.get_joke_info(netx_page_source)

    def get_next_page_url(self, source_html):
        next_page_url = Selector(text=source_html).xpath(
            "//*[@class='pagination']//span[@class='next']/../@href").extract_first()
        return next_page_url

    def save_item(self, item):
        # with open('./qiushi.txt', 'a') as fp:
        #     fp.write(json.dumps(item).replace('\n', '') + ',\n')
        joke_list.append(item.values())


if __name__ == '__main__':
    qiushi_spider = QiuShiSpiderRequest()
    source = qiushi_spider.get_source(BASE_URL)
    qiushi_spider.get_joke_info(source)

    col = [
        u'用户名',
        u'好笑数量',
        u'评论条数',
        u'评论内容',
        u'评论的点赞数量',
        u'正文',
        u'用户年龄',
        u'评论用户名',
        u'id',
        u'用户性别',
    ]

    df = pd.DataFrame(joke_list, columns=col)
    df.to_excel('./qiushi.xlsx', sheet_name=u'糗事百科')
