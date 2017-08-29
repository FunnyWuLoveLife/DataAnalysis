#!/usr/bin/env python
# encoding: utf-8

# @file: ID.3.py.py
# @time: 2017/8/29 16:43
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import math


class DecisionTree:
    """决策树相关类"""

    def __init__(self):
        """初始化类"""
        pass

    def create_tree(self, data, lable_data, feature):
        """生成决策树"""
        pass

    def find_maximum_gain_attribute(self):
        """寻找信息增益最大的20个属性"""

    def entropy(self, attributes, data, targetAttr):
        """计算信息熵"""
        val_freq = {}  # 记录值出现的次数
        data_entropy = 0.0  # 信息熵
        col_index = attributes.index(targetAttr)
        for row in data:
            val_freq.setdefault(row[col_index], 0)
            val_freq[row[col_index]] += 1

        for freq in val_freq.values():
            data_entropy += (-freq / len(data)) * math.log(freq / len(data), 2)  # 根据公式计算信息熵

        return data_entropy

    def gain(self):
        """计算信息增益"""
        pass


if __name__ == '__main__':


    pass
