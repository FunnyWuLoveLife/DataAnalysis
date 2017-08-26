#!/usr/bin/env python
# encoding: utf-8

# @file: DC.py.py
# @time: 2017/8/25 9:20
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import requests

cityGeoCoord = {}
city = "北京市海淀区上地十街10号"
cityGeoCoord.setdefault(city, [])
url = "http://api.map.baidu.com/geocoder/v2/?output=json&ak=nFfL1nyVWpEAQwdUqFdog0xo2vl4Vobw&address=" + city
temp = requests.get(url).json()
pass
