#!/usr/bin/env python
# encoding: utf-8

# @file: aaa.py
# @time: 2017/8/7 14:45
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm

import re
import collections

''''' 
从文件中读取内容，统计词频 
'''


def count_word(path):
    result = {}
    with open(path) as file_obj:
        all_the_text = file_obj.read()
        # 大写转小写
        all_the_text = all_the_text.lower()
        # 正则表达式替换特殊字符
        all_the_text = re.sub("\"|,|\.", "", all_the_text)

        for word in all_the_text.split():
            if word not in result:
                result[word] = 0
            result[word] += 1

        return result


''''' 
以词频倒序 
'''


def sort_by_count(d):
    # 字典排序
    d = collections.OrderedDict(sorted(d.items(), key=lambda t: -t[1]))
    return d


if __name__ == '__main__':
    file_name = "./text.txt"

    dword = count_word(file_name)
    dword = sort_by_count(dword)

    for key, value in dword.items():
        print key + ":%d" % value
