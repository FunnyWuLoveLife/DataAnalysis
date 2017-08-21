#!/usr/bin/env python
# encoding: utf-8

# @file: bbbb.py
# @time: 2017/8/6 16:43
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import pandas as pd
import pymongo
import time
import json
import charts
import numpy as np
import re
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import jieba.analyse
from PIL import Image
import matplotlib as plt

str_text = open(u'./text.txt', 'r').readlines()[0:200000]
str_text = '\n'.join(str_text)
str_text = str_text.decode('utf-8')
str_text = str_text\
    .replace(u'一个', '') \
    .replace(u'今人', '') \
    .replace(u'发表', '') \
    .replace(u'博文', '') \
    .replace(u'自己', '') \
    .replace(u'还是', '') \
    .replace(u'这样', '') \
    .replace(u'什么', '') \
    .replace(u'这个', '') \
    .replace(u'不是', '') \
    .replace(u'知道', '') \
    .replace(u'视频', '') \
    .replace(u'因为', '') \
    .replace(u'然后', '') \
    .replace(u'今天', '') \
    .replace(u'已经', '') \
    .replace(u'所以', '') \
    .replace(u'还有', '') \
    .replace(u'不会', '') \
    .replace(u'那么', '') \
    .replace(u'很多', '') \
    .replace(u'时候', '') \
    .replace(u'这么', '') \
    .replace(u'不能', '') \
    .replace(u'怎么', '') \
    .replace(u'看到', '') \
    .replace(u'这些', '') \
    .replace(u'视频', '') \
    .replace(u'但是', '')

wordcloud = WordCloud(
    font_path='./HYQiHei-25J.ttf',
    # 设置背景色
    background_color='white',
    #     mask=mask,
    max_words=3000,
    max_font_size=100,
    random_state=42
)
wordcloud = wordcloud.generate(str_text)
# wordcloud = wordcloud.generate(u"他 扮演 的 一个 什么 料 都 能 挖出来 的 媒体 记者")
wordcloud.to_file('wordcloud.png')

# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()
