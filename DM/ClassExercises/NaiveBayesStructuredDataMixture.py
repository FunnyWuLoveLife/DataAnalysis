#!/usr/bin/env python
# encoding: utf-8

# @file: NaiveBayesStructuredDataMixture.py
# @time: 2017/8/28 11:52
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import numpy as np
import math
import time
from DM.ClassExercises import Preprocessing


class Classifier:
    def __init__(self, dataFormat, header_info):
        """
        :param training_data_path: 训练数据路径
        :param dataFormat: 数据的格式，形如：attr attr attr attr class
        """

        # 获取数据行的格式
        self.format = dataFormat.strip().split("\t")
        # 获取数据特征维度信息
        self.header = header_info.strip().split("\t")
        # 先验概率
        self.prior = {}
        # 记录每个模型出现的次数
        self.classes = {}
        self.scatter = {}
        # 平滑处理参数
        self.alpha = 1
        # 条件概率
        self.conditional = {}
        # 开始训练

    def train(self, training_data_path):
        """
        训练分类器，训练方法
        :param training_data_path: 训练数据路径
        :return:
        """
        # 记录总共有多少条数据
        total = 0
        counts = {}
        # 训练数据文件名
        f = open(training_data_path, encoding='UTF-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            # 分割一条记录
            fields = line.strip().split(',')
            # 忽略的字段
            ignore = []
            # 特征向量
            vector = []
            # 分类
            category = ""
            # 根据给定的数据格式(这里已经转换为format列表)，查找给定数据的属性，并添加到特征向量中
            for idx, columnValue in enumerate(fields):
                if self.format[idx] == 'num':
                    vector.append(float(columnValue))
                elif self.format[idx] == 'attr':
                    vector.append(columnValue)
                elif self.format[idx] == 'content':
                    ignore.append(columnValue)
                elif self.format[idx] == 'class':
                    category = float(fields[idx])

            # 总的记录数增加一条
            total += 1
            # 为classes，counts设置该分类的一个默认值
            self.classes.setdefault(category, 0)
            counts.setdefault(category, {})
            # 分类数量加1
            self.classes[category] += 1
            # 处理各个特征，这些特征存储在特征向量vector中

            for idx, columnValue in enumerate(vector):
                feature_key = self.header[idx]
                # 区分连续值和，离散值，如果是特征是连续值，那么将所有值添加到数组，离散值则计算各个种类的个数
                if self.format[idx] == "content":
                    pass
                elif self.format[idx] == "num":
                    counts[category].setdefault(feature_key, [])
                    counts[category][feature_key].append(columnValue)
                elif self.format[idx] == 'attr':
                    self.scatter.setdefault(feature_key, {})
                    self.scatter[feature_key].setdefault(columnValue, 0)
                    self.scatter[feature_key][columnValue] += 0

                    counts[category].setdefault(feature_key, {})
                    counts[category][feature_key].setdefault(columnValue, 0)
                    counts[category][feature_key][columnValue] += 1

        # 计数结束，开始计算概率
        # 计算先验概率P(h)
        for (category, count) in self.classes.items():
            self.prior[category] = count / total

        # 计算条件概率P(h|D)
        for (category, columns) in counts.items():
            self.conditional.setdefault(category, {})

            for (col, valueCounts) in columns.items():
                self.conditional[category].setdefault(col, {})
                # 这里需要区分连续性还是离散型特征，离散型直接计算条件概率，连续计算方差和均值
                idx = self.header.index(col)
                if self.format[idx] == "content":
                    pass
                elif self.format[idx] == "num":
                    self.conditional[category][col]["mu"] = np.array(valueCounts).mean()  # 均值
                    self.conditional[category][col]["var"] = np.array(valueCounts).var()  # 方差
                elif self.format[idx] == 'attr':
                    for (attrValue, count) in valueCounts.items():
                        self.conditional[category][col][attrValue] = (
                            (count + self.alpha) / (
                                self.classes[category] + self.alpha * len(self.scatter[col])))

    def classify(self, itemVector):
        """返回itemVector所属类别"""
        results = []
        for (category, prior) in self.prior.items():
            prob = math.log(prior)
            for idx, attrValue in enumerate(itemVector):
                feature_key = self.header[idx]
                if self.format[idx] == "content":
                    pass
                elif self.format[idx] == "num":
                    mu = self.conditional[category][feature_key]["mu"]
                    var = self.conditional[category][feature_key]["var"]
                    # 解决方差为0 的情况
                    if var == 0:
                        var = 1
                        mu = 0
                    prob = prob + self.calculate_continuous_prob(float(attrValue), mu, var)
                elif self.format[idx] == 'attr':
                    if attrValue not in self.conditional[category][feature_key]:
                        prob = prob + (
                            self.alpha / (
                                self.classes[category] + self.alpha * len(self.scatter[feature_key])))
                    else:
                        prob = prob + math.log(self.conditional[category][feature_key][attrValue])
            results.append((prob, category))
        # 返回概率最高的结果
        return max(results)

    def calculate_continuous_prob(self, x, mu, var):
        a = math.log(2 * math.pi)
        b = math.log(var)
        d = ((x - mu) ** 2 / var)
        prob = -0.5 * (a + b + d)
        return prob


if __name__ == '__main__':
    start_time = time.time()
    dataFormat = open("../DataSet/character/dataFormat").readline()
    header_info = open("../DataSet/character/header_info").readline()
    c = Classifier(dataFormat, header_info)
    c.train("../DataSet/character/train_data.csv")

    test_data = [line.replace('\n', "").split(",") for line in open("../DataSet/character/test_data.csv")]
    result = {
        "T": {
            "total": 0,
            "yes": 0,
            "failure": 0
        },
        "F": {
            "total": 0,
            "yes": 0,
            "failure": 0
        }
    }

    for idx, one in enumerate(test_data):
        print("开始对第", idx + 1, "条测试记录分类")
        (logValue, lable) = c.classify(one[:1138])
        if float(one[1138]) == 1:
            result["T"]["total"] += 1
            if float(one[1138]) == lable:
                result["T"]["yes"] += 1
            else:
                result["T"]["failure"] += 1
        elif float(one[1138]) == 0:
            result["F"]["total"] += 1
            if float(one[1138]) == lable:
                result["F"]["yes"] += 1
            else:
                result["F"]["failure"] += 1

    print("分类结果:", result)
    end_time = time.time()
    print("消耗时间:", end_time - start_time)
