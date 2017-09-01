#!/usr/bin/env python
# encoding: utf-8

# @file: LinearRegression.py
# @time: 2017/8/31 17:02
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import math
from numpy import mat
from numpy import zeros


def logisticFun(x, w):  # x: Fx1, w: Fx1
    return 1 / (1 + math.exp(-w.T * x))


def lossFun(X, y, w, r):  # X: NxF, y:Nx1, w:Fx1
    numSamples = len(y)
    loss = 0
    for i in range(numSamples):
        x_i = X[i, :]  # x: 1xF
        y_i = y[i]
        loss += (y_i * x_i * w - math.log(1 + math.exp(x_i * w)))
    loss = loss / numSamples
    return -loss + r * math.sqrt(w.T * w)


def lossGrad(X, y, w, r):  # X: NxF, y:Nx1, w:Fx1
    numSamples, F = X.shape
    # grad = np.mat.zeros((F, 1))
    grad = mat(zeros((F, 1)))

    for i in range(numSamples):
        x_i = X[i, :].T  # x: 1xF
        y_i = y[i]
        y_pred = logisticFun(x_i, w)
        grad += (y_i - y_pred) * x_i
    grad /= numSamples
    return -grad + 2 * r * w


def train(X, y):
    numSamples, F = X.shape
    w = mat(zeros((F, 1)))
    # w = np.matlib.randn((F, 1))
    maxIter = 100
    r = 0.2
    loss = lossFun(X, y, w, r)
    print('init: ', loss)
    for it in range(maxIter):
        grad = lossGrad(X, y, w, r)
        alpha = 0.2
        for j in range(10):
            w_tmp = w - alpha * grad
            loss_tmp = lossFun(X, y, w_tmp, r)
            if loss_tmp < loss:
                w = w_tmp
                loss = loss_tmp
                break
            else:
                alpha /= 2.
        print('iteration ' + str(it) + ": " + str(loss))
    return w


def score(X, y, w):
    numSamples = len(y)
    hits = 0.
    for i in range(numSamples):
        x_i = X[i, :].T  # x: 1xF
        y_i = y[i]
        y_pred = logisticFun(x_i, w)
        y_pred = 0 if y_pred < 0.5 else 1
        if y_i == y_pred:
            hits += 1.
    return hits / numSamples
