#!/usr/bin/env python
# encoding: utf-8

# @file: qiushi.py
# @time: 2017/7/29 14:38
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import json
import pandas as pd


class QiuShi:
    def run(self):
        path = '../QiuShi_Spider/qiushi_user_info.json'
        data = [json.loads(line) for line in open(path)]
        data = pd.DataFrame(data)
        print data
        pass


if __name__ == '__main__':
    qiushi = QiuShi()
    qiushi.run()
