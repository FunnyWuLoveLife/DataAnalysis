#!/usr/bin/env python
# encoding: utf-8

# @file: TestData.py
# @time: 2017/8/31 9:11
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
from DM.ClassExercises.v2.LoadData import *
from DM.ClassExercises.v2 import Preprocessing
from DM.ClassExercises.v2.Bayes import Bayes
from DM.ClassExercises.v2 import LinearRegression


def testBayes():
    featType = loadFeatType("../../DataSet/character/features_type.csv")
    typeList, uids, X = loadTranX("../../DataSet/character/train_x.csv", featType)
    dataY = loadTrainY("../../DataSet/character/train_y.csv", uids)
    dataX, typeList = Preprocessing.fit(typeList=typeList, X=X, scaler=True)
    splitPoint = int(0.8 * dataY.size)
    train_x = dataX[:splitPoint]
    train_y = dataY[:splitPoint]
    devX = dataX[splitPoint:]
    devy = dataY[splitPoint:]
    model = Bayes(2, typeList)
    model.fit(train_x, train_y)
    print('score on train ', model.scores(train_x, train_y))
    print('score on dev ', model.scores(devX, devy))


def testLinearRegression():
    featType = loadFeatType("../../DataSet/character/features_type.csv")
    typeList, uids, X = loadTranX("../../DataSet/character/train_x.csv", featType)
    dataY = loadTrainY("../../DataSet/character/train_y.csv", uids)
    dataX, typeList = Preprocessing.fit(typeList=typeList, X=X, scaler=True)
    splitPoint = int(0.8 * dataY.size)
    train_x = np.matrix(dataX[:splitPoint])
    train_y = dataY[:splitPoint]
    devX = np.matrix(dataX[splitPoint:])
    devy = dataY[splitPoint:]

    w = LinearRegression.train(train_x, train_y)
    print('score on train ', LinearRegression.score(train_x, train_y, w))
    print('score on dev ', LinearRegression.score(devX, devy, w))
    pass


def testPCA():
    featType = loadFeatType("../../DataSet/character/features_type.csv")
    typeList, uids, X = loadTranX("../../DataSet/character/train_x.csv", featType)
    dataY = loadTrainY("../../DataSet/character/train_y.csv", uids)
    dataX, typeList = Preprocessing.fit(typeList=typeList, X=X, scaler=True)
    k = 300  # 保留的特征维度
    dataX = Preprocessing.pca(k, dataX)


if __name__ == '__main__':
    # testLinearRegression()
    testPCA()
    pass
