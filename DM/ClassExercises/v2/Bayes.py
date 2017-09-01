#!/usr/bin/env python
# encoding: utf-8

# @file: Bayes.py
# @time: 2017/8/31 16:29
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm


import math
import numpy as np

LOG_ZERO = math.log(1e-4)  # floor


class Normal:
    def __init__(self, mu=0, var=1):
        self.mu = mu
        self.var = var  # it's variance, not standard deviation

    def fit(self, xarr, yarr, ylabel):
        self.mu = 0
        self.var = 0
        num = 0
        for i, x in enumerate(xarr):
            if yarr[i] != ylabel:
                continue
            num += 1
            self.mu += x
        if num == 0:
            self.mu = 0
            self.var = 1
            return
        self.mu /= num

        for i, x in enumerate(xarr):
            if yarr[i] != ylabel:
                continue
            self.var += (x - self.mu) ** 2
        self.var /= num
        if self.var <= 0:
            self.var = 1

    def predict(self, x):  # p(xi | y = ?)
        return math.exp(self.predictLog(x))

    def predictLog(self, x):
        dif = x - self.mu
        return -0.5 * (math.log(2 * math.pi) + math.log(self.var) + dif * dif / self.var)


class Multinomial:
    probs = {}
    N = 0
    alpha = 1.0

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, xarr, yarr, ylabel):
        counts = {}
        num = 0
        cats = set()
        for i, x in enumerate(xarr):
            cats.add(x)
            if yarr[i] != ylabel:
                continue
            num += 1.
            if x in counts:
                counts[x] += 1.
            else:
                counts[x] = 1.
        nCats = len(cats)
        for x in cats:
            if x in counts:
                cnt = counts[x]
                self.probs[x] = (cnt + self.alpha) * 1.0 / (num + self.alpha * nCats)  # todo, smoothing
            else:
                self.probs[x] = self.alpha / (num + self.alpha * nCats)

    def predict(self, x):
        return self.probs[x]

    def predictLog(self, x):
        return math.log(self.probs[x])


class Bayes:
    typLst = []
    dist = None
    totalProbs = {}
    totalPriors = {}

    def __init__(self, nLabels, typLst, dist='normal'):
        self.nLabels = nLabels
        self.typLst = typLst
        self.dist = dist

    def fit(self, X, y):
        for j, typ in enumerate(self.typLst):
            if typ == 0:  # num
                gau4neg = Normal()
                gau4pos = Normal()
                gau4neg.fit(X[:, j], y, ylabel=0)
                gau4pos.fit(X[:, j], y, ylabel=1)
                self.totalProbs[j] = (gau4neg, gau4pos)
            if typ == 1:  # cat
                mult4neg = Multinomial()
                mult4pos = Multinomial()
                mult4neg.fit(X[:, j], y, ylabel=0)
                mult4pos.fit(X[:, j], y, ylabel=1)
                self.totalProbs[j] = (mult4neg, mult4pos)
        numPos = np.sum(y)
        numTot = len(y)
        numNeg = numTot - numPos
        self.totalPriors[0] = numNeg / numTot
        self.totalPriors[1] = numPos / numTot

    def predict(self, featVec):
        totalLog4Neg = math.log(self.totalPriors[0])
        totalLog4Pos = math.log(self.totalPriors[1])
        for j, x in enumerate(featVec):
            totalLog4Neg += self.totalProbs[j][0].predictLog(x)
            totalLog4Pos += self.totalProbs[j][1].predictLog(x)
        return 0 if totalLog4Neg > totalLog4Pos else 1

    def predicts(self, X):
        pred = []
        for x in X:
            pred.append(self.predict(x))
        return pred

    def scores(self, X, y):
        pred = self.predicts(X)
        hits = 0
        for p, t in zip(pred, y):
            if p == t:
                hits += 1
        return hits * 1.0 / len(y)
