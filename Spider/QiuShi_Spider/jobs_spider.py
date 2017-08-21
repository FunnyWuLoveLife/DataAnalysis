#!/usr/bin/env python
# encoding: utf-8

# @file: jobs_spider.py
# @time: 2017/7/19 10:11
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm

import requests
import json
import re
from lxml import etree
import time
from scrapy import Selector

BASE_URL = 'http://cd.58.com'


class JobsSpider:
    def __init__(self):
        pass

    def run(self):
        list = [u'服务员']
        url_list = []
        for key in list:
            result = self.get_ares_url(
                'http://cd.58.com/job/?key=' + key + '&final=1&jump=1&PGTID=0d302408-0006-60c8-a796-885f95d56f4f&ClickID=2')
            url_list.extend(result)
            time.sleep(2)
        for key, value in url_list:
            self.get_jobs(value, key)
        return

    def get_ares_url(self, url):
        time.sleep(2)
        url_list = []
        print  u'开始获取各区域URL'
        response = requests.get(url, self.get_request_headers())
        if response.status_code is not 200:
            print u'请求出错了，错误代码:', response.status_code
            return

        body = Selector(text=response.text)
        lis = body.xpath('//*[@id="filter"]/div[2]/dl[2]/dd/ul/li|//*[@id="filterArea"]/ul/li')[1:]
        if lis:
            for li in lis:
                key = li.xpath("./a/text()").extract_first()
                value = li.xpath("./a/@href").extract_first()
                result = re.search(r'&Host=\S*', value)
                if result:
                    value = value.replace(result.group(), '')
                    url_list.append((key, value))
        else:
            with open('./2.html', 'w') as fp:
                fp.write(response.content)
            print u'页面出错啦，数据抓取失败'

        return url_list

    def get_jobs(self, url, ares):

        print u'开始爬取URL为: ', url, ' 的页面'
        response = requests.get(url, self.get_request_headers(), timeout=30)
        if response.status_code is not 200:
            print u'请求出错了，错误代码:', response.status_code
            return
        body = Selector(text=response.text)

        # with open('./1.html', 'w') as fp:
        #     fp.write(response.content)
        #     return

        job_list_divs = body.xpath("//ul[@id='list_con']/li |//ul[@id='list_con']/dl")
        job_item = self.get_item()
        job_item[u'区域'] = ares
        for div in job_list_divs:
            job_item[u'岗位名字'] = div.xpath("./div[1]/div[1]/a/span[@class='name']/text()").extract_first()
            job_item[u'薪资'] = div.xpath("string(.//p[@class='job_salary'])").extract_first()
            job_item[u'详情页'] = div.xpath("./div[1]/div[1]/a/@href").extract_first()
            job_item[u'公司名字'] = div.xpath(
                "./div[@class='item_con job_comp']/div[@class='comp_name']/a/@title").extract_first()
            job_item[u'职位'] = div.xpath("./div[2]/p[@class='job_require']/span[1]/text()").extract_first()
            job_item[u'学历'] = div.xpath("./div[2]/p[@class='job_require']/span[2]/text()").extract_first()
            job_item[u'经验'] = div.xpath("./div[2]/p[@class='job_require']/span[3]/text()").extract_first()
            job_item[u'更新时间'] = div.xpath(
                "string(./dd[@class='w68']|//*[@id='infolist']/dl[1]/dd[4]|./span)").extract_first()
            self.get_details(job_item)
            time.sleep(1)

        time.sleep(1)

        # 下一页
        next_page_url = body.xpath(
            '//div[@class="leftbar"]/div[@class="pagerout"]/div[@class="pager"]/a[@class="next"]/@href').extract_first()
        if next_page_url:
            result = re.search(r'&Host=\S*', next_page_url)
            if result:
                next_page_url = next_page_url.replace(result.group(), '')
            self.get_jobs(next_page_url, ares)

        return

    def get_details(self, item):

        url = item[u'详情页'].replace('http://cd.58.com', 'http://m.58.com/cd')
        print u'开始爬取详情页URL为: ', url, ' 的页面'
        response = requests.get(url, self.get_request_headers())
        if response.status_code is not 200:
            print u'请求出错了，错误代码:', response.status_code
            return
        body = Selector(text=response.content)

        infos_selecotr = body.xpath("//*[@id='nav1']/section[@class='job_con']/ul")
        key = infos_selecotr.xpath("./li[2]/span[@class='attrValue']/text()").extract_first()
        if key:
            item[u'招聘人数'] = key
        item[u'地点'] = infos_selecotr.xpath("string(./li[3]/span[@class='attrValue dizhiValue'])").extract_first()
        item[u'福利'] = infos_selecotr.xpath(
            "string(./li[@class='fuli attrName']/div[@class='fulivalue attrValue'])").extract_first()
        item[u'电话'] = infos_selecotr.xpath("//*[@id='contact_phone']/@phoneno").extract_first()

        company_selector = body.xpath("//section[@class='dcompany_open']/div[@class='company_con btOnepx']")
        item[u'公司规模'] = company_selector.xpath("./ul/li[1]/span[2]/text()").extract_first()
        item[u'公司性质'] = company_selector.xpath("./ul/li[2]/span[2]/text()").extract_first()
        item[u'公司行业'] = company_selector.xpath("./ul/li[3]/span[2]/text()").extract_first()
        item[u'公司地址'] = company_selector.xpath("./ul/li[4]/span[2]/text()").extract_first()
        item[u'公司简介'] = company_selector.xpath("string(./ul/p)").extract_first()
        item[u'职位简介'] = body.xpath("string(//section[@class='pos']/div[1]/div[2])").extract_first()
        item[u'联系人'] = body.xpath(
            "//div[@class='body_div']/section[@class='company']/div[@class='com']/div/div[3]/span[2]").extract_first()
        self.write_file(item)
        pass

    def get_request_headers(self):
        '''获取request请求header'''
        headers = {
            'Host': 'cd.58.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Cookie': 'id58=BrDjn1liPZg+VbUPZc3y1g==; ipcity=cd%7C%u6210%u90FD%7C0; als=0; commonTopbar_myfeet_tooltip=end; wmda_uuid=105032707ebbf9fbb1c94dbcfddede07; wmda_new_uuid=1; sessionid=4206460a-ad82-4f18-9ba8-97ac5b7476d7; cookieuid=deae95f1-0e44-4979-8756-13ba18715cd7; ishome=true; m58comvp=t19v115.159.229.21; bj58_id58s="dG13R0ZCYW5jR0lHNTIxMA=="; gr_user_id=efbd2559-bef5-4f09-aef8-a80e348214ae; jl_abtest_resumedown_m=A; jl_ab_key=e2f1bcc29097847348253379290a0c44; from=""; cookieuid1=c5/ni1luxD6+A0Y4BkRCAg==; scancat=28924%2C-%2C13913%2C13931%2C13915; job_detail_resume_guide_show=1; job_detail_resume_guide_close=1; wmda_visited_projects=%3B1731916484865%3B1409632296065; Hm_lvt_e2d6b2d0ec536275bb1e37b421085803=1500433097; Hm_lpvt_e2d6b2d0ec536275bb1e37b421085803=1500434309; zscom=%5B0%2C0%2C0%2C0%5D; final_history=30390315837385%2C16134798457608; GA_GTID=0d40219d-0006-66d0-5958-fd279834a14e; _ga=GA1.2.1552840465.1500433097; _gid=GA1.2.892374917.1500433097; selectcity=yes; mcity=cd; mcityName=%E6%88%90%E9%83%BD; nearCity=%5B%7B%22cityName%22%3A%22%E6%88%90%E9%83%BD%22%2C%22city%22%3A%22cd%22%7D%5D; job_detail_show_time=20; hasLaunchPage=%7Cindex%7Cc_qzzp%7Cd_qzzp_zplvyoujiudian_29714328073040%7C; launchFlag=3; Hm_lvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1500431104; Hm_lpvt_5a7a7bfd6e7dfd9438b9023d5a6a4a96=1500451020; abtest="zp_zhuzhan_pc_detail_template=A"; 58home=cd; bj58_new_session=0; bj58_init_refer="http://cd.58.com/job/pn49/?key=%E6%9C%8D%E5%8A%A1%E5%91%98&final=1&jump=1&PGTID=0d302408-0006-6dfc-dc17-485d4e61ef07&ClickID=4"; bj58_new_uv=3; gr_session_id_b4113ecf7096b7d6=c643759e-25f3-4c01-923c-7545dd683155; city=cd; wmda_session_id=1500449255583-cefc3268-e525-664a; commontopbar_city=102%7C%u6210%u90FD%7Ccd; 58tj_uuid=b364c621-16cb-4b55-b5bf-e31e23f9a5d1; new_session=0; new_uv=2; utm_source=; spm=; init_refer='
        }
        return headers

    def write_file(self, item):

        for key in item.keys():
            if item[key]:
                item[key] = item[key].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
        json_item = json.dumps(item, ensure_ascii=False)
        json_item_utf8 = json_item.encode(encoding='UTF-8')
        with open('./jobs1.json', 'a') as fp:
            fp.write(json_item_utf8)
            fp.write(',\n')
        print u'成功爬取第id为: ' + item[u'详情页'] + u' 的职位信息'

    def get_item(self):
        job_item = {
            u'区域': '',
            u'详情页': '',
            u'公司名字': '',
            u'岗位名字': '',
            u'薪资': '',
            u'更新时间': '',
            u'职位': '',
            u'经验': '',
            u'招聘人数': '',
            u'学历': '',
            u'地点': '',
            u'福利': '',
            u'电话': '',
            u'联系人': '',
            u'公司规模': '',
            u'公司性质': '',
            u'公司行业': '',
            u'公司地址': '',
            u'公司简介': '',
            u'职位简介': ''
        }
        return job_item


if __name__ == '__main__':
    jobs_spider = JobsSpider()
    jobs_spider.run()
