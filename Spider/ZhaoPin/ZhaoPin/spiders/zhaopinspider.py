#!/usr/bin/env python
# encoding: utf-8

# @file: zhaopinspider.py
# @time: 2017/7/20 20:50
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import scrapy
from ZhaoPin.items import ZhaopinItem


class ZhaoPinSpider(scrapy.Spider):
    name = 'ZhaoPin'
    start_urls = [
        'http://sou.zhaopin.com/jobs/searchresult.ashx'
    ]

    def parse(self, response):
        """
        入口地址解析函数，该函数解析职位类别，然后迭代该职位类型的url出去，
        在迭代出去的Request对象的meta属性中添加一个item，该item中携带职位类型的值
        :param response:
        :return:
        """
        divs = response.xpath("//div[@class='moresearch_main fl']/ul/li[5]/div/a")
        for div in divs:
            item = ZhaopinItem()
            url = 'http://sou.zhaopin.com' + div.xpath("./@href").extract_first()
            item['position_category'] = div.xpath("./text()").extract_first()
            page_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'sou.zhaopin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Referer': response.url,
            }
            yield scrapy.Request(url, self.parse_areas, headers=page_headers, meta={'item': item})

    def parse_areas(self, response):
        """
        区域url解析函数，接收一个response对象，这个response对象中的meta属性中携带有item属性
        这个item属性中有职位类型的值，然后该函数获取区域url，获取到后迭代取出，并且将携带有职位类型，区域信息的item也跟随元数据一起传输
        :param response:
        :return:
        """
        divs = response.xpath(
            "//div[@class='newlist_list1 ']/div[@class='clearfix']/div[@class='search_newlist_topmain1 fl']/a")
        item = response.meta['item']
        for div in divs[1:]:
            item['area'] = div.xpath("./text()").extract_first()
            area_url = 'http://sou.zhaopin.com' + div.xpath("./@href").extract_first()
            page_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'sou.zhaopin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Referer': response.url,
            }
            yield scrapy.Request(area_url, self.parse_job_list, headers=page_headers, meta={'item': item})

    def parse_job_list(self, response):
        """
        获取职位详细列表，用于接收区域解析函数的请求返回对象，
        并且解析职位详情的url并迭代出去，携带一个在职位列表页获取到的数据的item
        :param response:
        :return:
        """
        lis = response.xpath("//*[@id='newlist_list_content_table']/table")
        item = response.meta['item']

        for li in lis[2:]:
            item['detail_url'] = li.xpath("string(.//td[@class='zwmc']/div/a/@href)").extract_first()
            item['company_name'] = li.xpath("string(.//td[@class='gsmc'])").extract_first()
            item['position_name'] = li.xpath("string(.//td[@class='zwmc'])").extract_first()
            item['salary'] = li.xpath("string(.//td[@class='zwyx'])").extract_first()
            item['update_tiem'] = li.xpath("string(.//td[@class='gxsj'])").extract_first()
            item['work_address'] = li.xpath("string(.//td[@class='gzdd'])").extract_first()

            detail_url = item['detail_url']
            headers = {
                'Host': 'jobs.zhaopin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Referer': response.url
            }
            yield scrapy.Request(detail_url, callback=self.parse_detail, headers=headers, meta={'item': item})
        next_page_url = response.xpath("//*[@class='pagesDown-pos']/a[@class='next-page']/@href").extract_first()
        if next_page_url is not None:
            page_headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Host': 'sou.zhaopin.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                'Referer': response.url,
            }
            yield scrapy.Request(next_page_url, callback=self.parse_job_list, headers=page_headers)

    def parse_detail(self, response):
        """
        解析详情页，接收的response对象有元数据包含区域信息和职位列表页获取得到的数据，
        在该页面获取详情页信息后将item数据跌代到管道pipelines中进行处理
        :param response:
        :return:
        """
        item = response.meta['item']
        item['experience'] = response.xpath(
            "//div[@class='terminalpage clearfix']//ul[@class='terminal-ul clearfix']/li[5]/strong/text()").extract_first()
        item['welfare'] = ",".join(response.xpath(
            "//div[@class='top-fixed-box']//div[@class='inner-left fl']/div[@class='welfare-tab-box']/span/text()").extract())
        item['hiring_number'] = response.xpath(
            "//div[@class='terminalpage clearfix']//ul[@class='terminal-ul clearfix']/li[7]/strong/text()").extract_first()
        item['degree'] = response.xpath(
            "string(//div[@class='terminalpage clearfix']//ul[@class='terminal-ul clearfix']/li[6]/strong)").extract_first()
        item['company_scal'] = response.xpath("//div[@class='company-box']/ul/li[1]/strong/text()").extract_first()
        item['company_property'] = response.xpath("//div[@class='company-box']/ul/li[2]/strong/text()").extract_first()
        item['company_profession'] = response.xpath(
            "//div[@class='company-box']/ul/li[3]/strong/text()").extract_first()
        item['company_address'] = response.xpath("//div[@class='company-box']/ul/li[4]/strong/text()").extract_first()
        item['position_intro'] = response.xpath(
            "string(//div[@class='terminalpage-main clearfix']//div[@class='tab-inner-cont'][1])").extract_first()
        item['company_intro'] = response.xpath(
            "string(//div[@class='terminalpage-main clearfix']//div[@class='tab-inner-cont'][2])").extract_first()
        yield item
