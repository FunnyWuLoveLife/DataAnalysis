#!/usr/bin/env python
# encoding: utf-8

# @file: python_io.py
# @time: 2017/7/17 16:09
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import json

path = "./io.html"


# if not os.path.exists(path):
#     os.makedirs('./io')
# fp = open('./io.txt', mode='a')
# fp.write('写文件\n')
# fp.close()


def write_str_to_file(str):
    fp = open(path, mode='a')
    fp.write(str)
    fp.close()


def read_file():
    """
    with as 会自动关闭文件
    :return:
    """
    with open(path, 'r') as fp:
        print fp.read()


# write_str_to_file('<html><body>这是一个html文件</body></html>')

# read_file()

list = list()
dict = {'name': 'FunnyWu', 'age': 24}
list.append(dict)
list.append(dict)
list.append(dict)
list.append(dict)
dict2 = {'name': 'FunnyWu', 'age': 24, 'followers': [1, 2, 3]}
list.append(dict2)

print json.dumps(list)
