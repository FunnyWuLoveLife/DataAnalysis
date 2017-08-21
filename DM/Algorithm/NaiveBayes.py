#!/usr/bin/env python
# encoding: utf-8

# @file: NaiveBayes.py
# @time: 2017/8/21 9:02
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm


class Classifier:
    def __init__(self, dataFormat):
        """
        :param training_data_path: 训练数据路径
        :param dataFormat: 数据的格式，形如：attr attr attr attr class
        """

        # 获取数据行的格式
        self.format = dataFormat.strip().split("\t")
        # 先验概率
        self.prior = {}
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
        # 记录每个模型出现的次数
        classes = {}
        # 记录条件概率的次数
        counts = {}

        # 训练数据文件名
        f = open(training_data_path, encoding='UTF-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            # 分割一条记录
            fields = line.strip().split('\t')
            # 忽略的字段
            ignore = []
            # 特征向量
            vector = []
            # 分类
            category = ""
            # 根据给定的数据格式(这里已经转换为format列表)，查找给定数据的属性，并添加到特征向量中
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(float(fields[i]))
                elif self.format[i] == 'attr':
                    vector.append(fields[i])
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    category = fields[i]

            # 总的记录数增加一条
            total += 1
            # 为classes，counts设置该分类的一个默认值
            classes.setdefault(category, 0)
            counts.setdefault(category, {})
            # 分类数量加1
            classes[category] += 1
            # 处理各个特征，这些特征存储在特征向量vector中
            col = 0
            for columnValue in vector:
                col += 1
                counts[category].setdefault(col, {})
                counts[category][col].setdefault(columnValue, 0)
                counts[category][col][columnValue] += 1

        # 计数结束，开始计算概率
        # 计算先验概率P(h)
        for (category, count) in classes.items():
            self.prior[category] = count / total
        # 计算条件概率P(h|D)
        for (category, columns) in counts.items():
            self.conditional.setdefault(category, {})
            for (col, valueCounts) in columns.items():
                self.conditional[category].setdefault(col, {})
                for (attrValue, count) in valueCounts.items():
                    self.conditional[category][col][attrValue] = (count / classes[category])

    def classify(self, itemVector):
        """返回itemVector所属类别"""
        results = []
        for (category, prior) in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if attrValue not in self.conditional[category][col]:
                    # 属性不存在，返回0概率
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            results.append((prob, category))
        # 返回概率最高的结果
        return max(results)[1]


if __name__ == '__main__':
    c = Classifier("attr\tattr\tattr\tattr\tclass")

    c.train("../DataSet/NaiveBayesTestData")

    print(c.classify(['health' 'moderate', 'moderate', 'yes']))
