
# coding: utf-8

# In[1]:


import os
import pandas as pd


# In[2]:


class Imputer:
    """缺失值处理方法"""

    def __init__(self, missing_value="NaN", ):
        """
        :param missing_value: 缺失值符合
        """
        self.missing_value = missing_value

    def fit(self, colValue, valueType="numeric", strategy="mean"):
        if valueType == "numeric":  # 处理数值型数据
            missing_value_index = []  # 缺失值索引
            if strategy == "mean":
                no_missing_sum = 0
                for idx, value in enumerate(colValue):
                    if value == self.missing_value:
                        missing_value_index.append(idx)  # 将缺失值得索引存储到列表，加快后期填补速率
                        continue
                    no_missing_sum += float(value)  # 对未缺失的值求和
                mu = no_missing_sum / (len(colValue) - len(missing_value_index))  # 求均值，未缺失的个数为总个数减缺失的数量
                for index in missing_value_index:  # 填补缺失值
                    colValue[index] = mu
        elif valueType == "category":  # 处理离散型数据
            if strategy == "mode":
                value_count = {}
                missing_value_index = []  # 缺失值索引
                for idx, value in enumerate(colValue):
                    if value[0] == "-":
                        missing_value_index.append(idx)  # 将缺失值得索引存储到列表，加快后期填补速率
                        continue
                    value_count.setdefault(value, 0)
                    value_count[value] += 1

                max_key, max_value = max(value_count.items(), key=lambda x: x[1])  # 使用max函数查找字典最大值那个
                for index in missing_value_index:  # 填补缺失值
                    colValue[index] = max_key
        else:
            raise TypeError("给定值类型错误")
        return colValue


# In[3]:


def load_train_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError()
    else:
        train_data = [line.strip().split(',') for line in open(path)]
    return train_data[1:], train_data[0]


def merge(train_x, train_y):
    for idx, value in enumerate(train_x):
        if value[0] == train_y[idx][0]:
            train_x[idx].append(train_y[idx][1])
        else:
            for train_row in train_y:
                if value[0] == train_row[0]:
                    train_x[idx].append(train_row[1])
    return train_x


def preprocessing(train_x, header_x, features_type):
    len_row = len(train_x)  # 多少行
    len_col = len(train_x[0][1:])  # 多少列
    imputer = Imputer("-1")
    result_data = train_x
    for col in range(1, len_col):
        col_arr = []
        for row in range(len_row):
            col_arr.append(train_x[row][col])
        if features_type[col][0] == header_x[col]:
            col_value = imputer.fit(colValue=col_arr, valueType=features_type[col][1], strategy=features_type[col][1])
            for row in range(len_row):
                result_data[row][col] = col_value[row]
    return result_data

def get_train_data():
    path = "../DataSet/character/clean_data_no_label.csv"
    if os.path.exists(path):
        clean_data_no_label = [line.split(",") for line in open(path)]
        attributes = clean_data_no_label[0]
        train_data = clean_data_no_label[1:]
        return attributes,train_data
    else:
        train_x, header_x = load_train_data("../DataSet/character/train_x.csv")
        features_type, header_type = load_train_data("../DataSet/character/features_type.csv")
        train_data = preprocessing(train_x=train_x, header_x=header_x[1:], features_type=features_type)
        return header_x,train_data

