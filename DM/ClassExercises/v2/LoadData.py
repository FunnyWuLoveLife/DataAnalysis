#!/usr/bin/env python
# encoding: utf-8

# @file: LoadData.py
# @time: 2017/8/31 0:14
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import numpy as np


def loadFeatType(fname):
    """加载特征值类型数据
    :param fname: str 文件路径
    :return: dict key:特征名称 value: 特征值类型{numeric,category}
    """
    featType = {}
    with open(fname) as f:
        header = f.readline()  # 把文件头读取出来 抛弃
        for line in f.readlines():
            k, v = line.strip().replace('"', "").replace('\n', "").split(',')
            # featType[k] = v
            if k[:1] == 'x':
                featType[k] = 0 if v == 'numeric' else 1  # 0: numeric, 1: categorical
    return featType


def loadTranX(fname, featType):
    """加载训练数据
    :param fname: str 文件路径
    :param featType: dict 特征值类型字典,key:特征名称 value: 特征值类型{numeric,category}
    :return: tuple (typeList:特征值类型 ,uids:记录的uid列表，X:m*n维度多维数组 m为特征数，n为记录数 )
    """
    uids = []
    X = []
    typeList = []
    with open(fname) as fp:
        herder = fp.readline()
        typeList += [featType[field] for field in herder.strip().split(",")[1:]]  # 获取特征类型列表
        for line in fp.readlines():
            row = line.strip().replace('"', "").replace('\n', "").split(",")  # 获取一条记录的
            # 将数据记录成一个m*n维度多维数组 m为特征数，n为记录数
            # 并且把数据转换为相应的类型 耗时
            X.append(row[1:])
            uids.append(row[0])
    return typeList, uids, X


def loadTrainY(fname, uids):
    """根据文件路径和uid列表加载标签数据
    :param fname: str 文件路径
    :param uids: list uid列表,为了将标签和train对应起来
    :return: np.array 标签数据
    """
    labels = {}
    with open(fname) as f:
        header = f.readline()
        for line in f.readlines():
            uid, lab = line.strip().replace('"', "").replace('\n', "").split(',')
            labels[uid] = float(lab)
    return np.array([labels[uid] for uid in uids])
