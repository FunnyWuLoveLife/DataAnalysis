#!/usr/bin/env python
# encoding: utf-8

# @file: NaiveBayesUnstructuredData.py.py
# @time: 2017/8/21 16:28
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import codecs
import os
import math


class BayesText:
    def __init__(self, stopword_dir):
        """该类实现了朴素贝叶斯对文本分类的方法
        :param stopwordlist: 停止词列表
        """
        # 总词汇表
        self.vocabulary = {}
        # 概率
        self.prob = {}
        # 某个类别的总数量
        self.totals = {}
        # 停止词
        self.stopwords = {}

        self.categories = None

        # 获取停词列表
        print(os.times(), ":\tstart loading stopword list")
        f = open(stopword_dir)
        for line in f:
            self.stopwords[line.strip()] = 1
        f.close()

    def prepare(self, train_data_dir):
        """
        获取各分类的名称
        :param train_data_dir: 训练数据目录
        :return:
        """
        # 列出所有分类的名称
        categories = os.listdir(train_data_dir)
        # 将不是目录的元素过滤掉
        self.categories = [filename for filename in categories if os.path.isdir(train_data_dir + filename)]
        print(os.times(), ":\tstart reading train directory")
        for category in categories:
            (self.prob[category], self.totals[category]) = self.train(train_data_dir, category)

        # 删除出现次数小于3次的单词
        to_delete = []
        # 查找需要删除的单词
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                to_delete.append(word)
        # 删除单词
        for word in to_delete:
            del self.vocabulary[word]

        # 计算概率

        # 词汇库长度
        vocab_length = len(self.vocabulary)
        for category in self.categories:
            denominator = self.totals[category] + vocab_length
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (float(count + 1) / denominator)
        pass

    def train(self, train_data_dir, category):
        """计算分类下各单词出现的次数"""
        print(os.times(), ":\tstart training:", category)
        currentdir = train_data_dir + category
        # 获取该分类下所有文件
        files = os.listdir(currentdir)

        counts = {}
        total = 0

        for file in files:
            f = codecs.open(currentdir + '/' + file, 'r', 'iso8859-1')
            for line in f:
                tokens = line.split()
                for token in tokens:
                    # 删除标点符号，并将单词转换为小写
                    token = token.strip('\'".,?:->#()+_[]$<*^/').lower()
                    # 判断获取到的词是否属于停词
                    if token != '' and token not in self.stopwords:
                        # 设置总词汇库的默认值
                        self.vocabulary.setdefault(token, 0)
                        # 将总词汇库总该词数量+1
                        self.vocabulary[token] += 1
                        # 将该分类下这个词汇默认值设置为0
                        counts.setdefault(token, 0)
                        counts[token] += 1
                        # 该分类下词汇数量+1
                        total += 1
            f.close()
        return counts, total

    def classify(self, filename):
        results = {}
        for category in self.categories:
            results[category] = 0
        f = codecs.open(filename, 'r', 'iso8859-1')
        for line in f:
            tokens = line.split()
            for token in tokens:
                token = token.strip('\'".,?:->#()+_[]$<*^/').lower()
                if token in self.vocabulary:
                    for category in self.categories:
                        if self.prob[category][token] == 0:
                            print("%s %s" % (category, token))
                        results[category] += math.log(self.prob[category][token])
        f.close()
        results = list(results.items())
        results.sort(key=lambda tuple: tuple[1], reverse=True)
        # for debugging I can change this to give me the entire list
        return results[0][0]

    def test_category(self, directory, category):
        """测试给定路径下的所以文件的分类"""
        files = os.listdir(directory)
        # 总数
        total = 0
        # 正确分类的数量
        correct = 0
        for file in files:
            total += 1
            result = self.classify(directory + file)
            if result == category:
                correct += 1
        return correct, total

    def test(self, test_dir):
        """测试"""
        categories = os.listdir(test_dir)
        # 过滤掉不是目录的元素
        categories = [filename for filename in categories if os.path.isdir(test_dir + filename)]
        correct = 0
        total = 0
        for category in categories:
            (catCorrect, catTotal) = self.test_category(test_dir + category + '/', category)
            correct += catCorrect
            total += catTotal
        print("\n\nAccuracy is  %f%%  (%i test instances)" % ((float(correct) / total) * 100, total))
        pass


if __name__ == '__main__':
    bt = BayesText("../DataSet/20news-bydate/stoplist.txt")
    bt.prepare("../DataSet/20news-bydate/20news-bydate-train/")
    # 简单测试分类，可使用桶测试
    # result = bt.classify("../DataSet/20news-bydate/20news-bydate-test/comp.graphics/38758")
    bt.test("../DataSet/20news-bydate/20news-bydate-test/")
    pass
