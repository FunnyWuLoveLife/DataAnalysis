#!/usr/bin/env python
# encoding: utf-8

# @file: Preprocessing.py
# @time: 2017/8/30 23:14
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
from DM.ClassExercises.v2.LoadData import *
from sklearn.preprocessing import Imputer, OneHotEncoder
from sklearn.preprocessing import StandardScaler


def fit(self, typeList, X, imp4Num=None, imp4Cat=None, scaler=False, enc=False):
    """对数据进行预处理
    :param typeList: list 特征类型列表
    :param X: m*n list 数据
    :return:
    """
    featVecLst4Num = []
    featVecLst4Cat = []
    for row in X:
        featVec4Num = []
        featVec4Cat = []
        for typ, v in zip(typeList, row):
            if typ == 0:
                featVec4Num.append(np.nan if v == '-1' else float(v))  # 连续值转换为float,为空使用np.nan处理
            elif typ == 1:
                featVec4Cat.append(np.nan if v[0] == '-' else int(v))  # 离散值转换为int,为空使用np.nan处理
        featVecLst4Num.append(np.array(featVec4Num))
        featVecLst4Cat.append(np.array(featVec4Cat))
    featMat4Num = np.array(featVecLst4Num)
    featMat4Cat = np.array(featVecLst4Cat)

    catCount = sum(typeList)
    numCount = len(typeList) - catCount
    typeList = [0] * numCount + [1] * catCount

    # first deal with missing value
    if imp4Num is None:
        imp4Num = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp4Num.fit(featMat4Num)
    featMat4NumImp = imp4Num.transform(featMat4Num)

    if imp4Cat is None:
        imp4Cat = Imputer(missing_values='NaN', strategy='most_frequent', axis=0)
        imp4Cat.fit(featMat4Cat)
    featMat4CatImp = imp4Cat.transform(featMat4Cat)

    # second deal with scaling
    if scaler is True:
        scaler = StandardScaler()
        scaler.fit(featMat4NumImp)
        featMat4NumImp = scaler.transform(featMat4NumImp)

    # third one-hot encoding
    if enc is True:
        enc = OneHotEncoder()
        enc.fit(featMat4CatImp)
        featMat4CatImp = enc.transform(featMat4CatImp).toarray()  # scipy.sparse.csr.csr_matrix
    # concatenate numeric and categorical features
    newFeatMat = np.concatenate((featMat4NumImp, featMat4CatImp), axis=1)
    # return uids, newFeatMat, imp4Num, imp4Cat, scaler, enc
    return newFeatMat, typeList


def pca(self, k, dataX):
    """PCA降维
        设有m条n维的原始数据矩阵dataX。
        1.将原始数据按列组成n行m列矩阵X
        2.将X的每一行（代表一个属性字段）进行零均值化，即减去这一行的均值
        3.求出协方差矩阵 C = 1/m * dataX * dataXT
        4.求出协方差矩阵的特征值及对应的特征向量
        5.将特征向量按对应特征值大小从上到下按行排列成矩阵，取前k行组成矩阵P
        6.Y=PX即为降维到k维后的数据
    """
    dataX = np.matrix(dataX)
    m, n = dataX.shape
    X = dataX.T
    mu = np.mean(X, axis=1)  # axis=1 表示按行计算，返回的mu为一个 1 * n 维的均值ndarray对象
    for idx in range(n):  # 去均值
        X[idx] -= mu[idx]
    C = 1 / m * (X * X.T)
    eigenValues, eigenVectors = np.linalg.eig(C)  # 获取协方差矩阵特值e、特征值向量v
    idx = eigenValues.argsort()
    # eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:, idx]
    resultData = (eigenVectors[:k] * X).T
    return resultData
