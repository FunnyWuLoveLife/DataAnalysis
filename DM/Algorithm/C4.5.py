#!/usr/bin/env python
# encoding: utf-8

# @file: C4.5.py
# @time: 2017/8/21 8:52
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm


class Node:
    """决策树C4.5"""

    def __init__(self, parent=None, dataset=None):
        self.dataset = dataset  # 咯在该结点的训练集
        self.result = None  # 结果类标签
        self.attr = None  # 该结点分类属性ID
        self.childs = {}  # 该结点
