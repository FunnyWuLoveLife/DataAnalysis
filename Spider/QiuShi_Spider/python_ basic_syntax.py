#!/usr/bin/env python
# encoding: utf-8

# @file: python_ basic_syntax.py
# @time: 2017/7/17 11:41
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm


def get_sum(x, y):
    """
    求和
    :param x:
    :param y:
    :return:  x+y 的和
    """
    return x + y


def get_list_max_values(list):
    """
    求列表中的最大值
    :param list:
    :return: 最大值
    """
    max = list[0]
    for key in list:
        if key > max:
            max = key
    return max


def get_dict_keys_by_values(dict, values):
    """
    求给定字典中，给定值所对应的键,以列表形式返回
    :param dict: 给定字典
    :param values: 给定值
    :return: 对应键的列表
    """
    key_list = list()

    for key, value in dict.items():
        if value is values:
            key_list.append(key)
    return key_list


def sortedDictValues2(adict):
    """
    对字典排序，通过列表生成器，以key为依据排序
    :param adict:   给定字典
    :return:    排序完成后的字典
    """
    keys = adict.keys()
    keys.sort()
    return [adict[key] for key in keys]


dict = {'key5': 1, 'key2': 3, 'key3': 2, 'key4': 1, }


# print get_list_max_values([1, 2, 3, 8, 10, 23, 1])
# print get_dict_keys_by_values(dict, 1)
# print [1, 2] + [a for a in range(10) if a > 6][::]
