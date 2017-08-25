#!/usr/bin/env python
# encoding: utf-8

# @file: DC.py.py
# @time: 2017/8/25 9:20
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import pandas as pd

accident_data = pd.read_csv("dataset/accident_data.csv")
weather_data = pd.read_csv("dataset/weather_data.csv")
infringe_data = pd.read_csv("dataset/infringe_data.csv")

for i in range(21, 28):
    int_i = str(i)
    indexName = "Unnamed: " + int_i
    del accident_data[indexName]
for i in range(6, 13):
    int_i = str(i)
    indexName = "Unnamed: " + int_i
    del infringe_data[indexName]
print(accident_data)
