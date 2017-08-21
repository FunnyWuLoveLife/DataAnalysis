#!/usr/bin/env python
# encoding: utf-8

# @file: qiushi_user_info_by_requtest.py
# @time: 2017/7/18 17:24
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm

import requests
from scrapy import Selector
import json
import time
import re

BASE_URL = "https://www.qiushibaike.com/users/"

id_queue = [{30777231: False}]


class QiuShiUserInfo:
    def __init__(self):
        pass

    def get_user_info(self, url):
        herders = {
            'Host': 'www.qiushibaike.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        response = requests.get(url, headers=herders, verify=False)
        if response.status_code is not 200:
            print u'请求失败，请求错误码为:', response.status_code
            return

        body = Selector(text=response.text)
        user_info_selector = body.xpath("//*[@class='user-main clearfix']")
        if user_info_selector.xpath("string(//*[@class='user-main clearfix']//div[@class='user-header-cover'])"):
            user_info = {
                'username': user_info_selector.xpath(
                    "string(//*[@class='user-main clearfix']//div[@class='user-header-cover'])")
                    .extract_first().strip('\n'),
                'id': user_info_selector.xpath("//a[@class='user-header-avatar']/@href").extract_first().
                    replace('/users/', '').strip('/')
            }
            personal_data_divs = user_info_selector.xpath("./div[@class='user-col-left']/div")
            for key in personal_data_divs:
                for li in key.xpath('./ul/li'):
                    key = li.xpath('./span/text()').extract_first()
                    user_info[key] = li.xpath('./text()').extract_first()

            # 粉丝信息
            time.sleep(2)
            user_info['followers'] = self.get_followers(user_info['id'])
            self.write_file(user_info)
            return True
        else:
            return False

    def write_file(self, item):
        json_item = json.dumps(item, ensure_ascii=False)
        json_item_utf8 = json_item.encode(encoding='UTF-8')
        with open('./qiushi_user_info.json', 'a') as fp:
            fp.write(json_item_utf8)
            fp.write('\n')
        print u'成功爬取id为' + item['id'] + u'的用户信息\n'

    def write_id_to_queue(self, id):
        id = re.search(r"[0-9]+", id)
        if id:
            id = int(id.group())
            id_queue.append({id: False})
        else:
            print 'Id:', id, '错误，加入队列失败'

    def get_followers(self, id):
        base_follower_url = 'https://www.qiushibaike.com/users/'
        herders = {
            'Host': 'www.qiushibaike.com',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'zh - CN, zh;q = 0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': base_follower_url + id + '/'
        }
        follower_url = base_follower_url + id + '/followers/'
        response = requests.get(follower_url, headers=herders, verify=False)
        if response.status_code is not 200:
            print u'请求失败，请求错误码为:', response.status_code
            return
        body = Selector(text=response.text)

        follower = {'fans': [], 'focus': [], 'mutual_fans': []}

        qiu_friends_selector = body.xpath(
            "//div[@class='user-col-right']/div[1]/ul/li")
        focus = list()
        for li in qiu_friends_selector:
            # uid = li.xpath('./a[2]/@href')
            uid = li.xpath('./a[2]/@href').extract_first().replace('/users/', '').strip('/')
            self.write_id_to_queue(uid)  # 将爬取到的id添加到爬取队列
            username = li.xpath('./a[2]/text()').extract_first().strip('\n')
            focus.append({'id:': uid, 'username': username})
        follower['focus'] = focus

        fans_selector = body.xpath("//div[@class='user-col-right']/div[2]/ul/li")
        fans = list()
        for li in fans_selector:
            uid = li.xpath('./a[2]/@href').extract_first().replace('/users/', '').strip('/')
            self.write_id_to_queue(uid)  # 将爬取到的id添加到爬取队列
            username = li.xpath('./a[2]/text()').extract_first().strip('\n')
            fans.append({'id:': uid, 'username': username})
        follower['fans'] = fans

        mutual_fans_selector = body.xpath("//div[@class='user-col-right']/div[3]/ul/li")
        mutual_fans = list()
        for li in mutual_fans_selector:
            uid = li.xpath('./a[2]/@href').extract_first().replace('/users/', '').strip('/')
            self.write_id_to_queue(uid)  # 将爬取到的id添加到爬取队列
            username = li.xpath('./a[2]/text()').extract_first().strip('\n')
            mutual_fans.append({'id:': uid, 'username': username})
        follower['mutual_fans'] = mutual_fans

        return follower

    def run(self):
        for key in id_queue:
            for key2 in key:
                if not key[key2]:
                    print u'开始爬取id为', key2, u'的用户信息'
                    if self.get_user_info(BASE_URL + str(key2)):
                        id_queue.remove(key)  # 爬取完成删除该id信息
                    time.sleep(4)


if __name__ == '__main__':
    qiushi_user_info_spider = QiuShiUserInfo()
    qiushi_user_info_spider.run()
