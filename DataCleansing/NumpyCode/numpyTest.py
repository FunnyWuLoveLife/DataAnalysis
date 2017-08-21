#!/usr/bin/env python
# encoding: utf-8

# @file: numpyTest.py
# @time: 2017/7/25 22:35
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm
import numpy as np
import matplotlib

def main():
    lst = [[1, 3, 5, 7, 9], [2, 4, 6, 8, 10]]
    print type(lst)
    np_lst = np.array(lst, dtype=np.int)
    print np_lst.dtype
    print np_lst.shape
    print np_lst.ndim
    print np_lst.itemsize
    # 生成
    print np.zeros([3, 4])
    print np.ones([4, 9])
    print "三维:"
    print (np.random.rand(3, 4, 3))
    print (np.random.rand())
    print "RandInt:"
    print (np.random.randint(3, 10, 5))
    print "Randn:"
    print np.random.randn(2, 4)
    print "Choice:"
    print (np.random.choice([10, 20, 30, 33, 44], 3))
    print "Distribute:"
    print np.random.beta(1, 10, 100)
    # 操作
    lst = np.arange(1, 11).reshape([2, -1])
    print "指数:"
    print np.exp(lst)
    print "指数:"
    print np.exp2(lst)
    print "开方:"
    print np.sqrt(lst)
    print "Sin:"
    print np.sin(lst)
    print "对数:"
    print np.log(lst)

    lst = np.array([[2, 4, 8, 16, 32],
                    [64, 128, 256, 512, 1024]])

    print "和为:", lst.sum(axis=1)
    print "Max:", lst.max(axis=1)
    print "Min:", lst.min()

    a = np.array([[3., 1.],
                  [1., 2.]])
    b = np.asmatrix(a)

    print b
    c = b * b
    print c
    import pandas as pd

    data = pd.DataFrame({'group': ['a', 'b', 'b', 'd', 'e'], 'ouncea': [1, 2, 3, 4, 5, ]})
    from echarts import Echart, Legend, Bar, Axis

    chart = Echart('GDP', 'This is a fake chart')
    chart.use(Bar('China', [2, 3, 4, 5]))
    
    chart.use(Axis('category', 'bottom', data=['Nov', 'Dec', 'Jan', 'Feb']))
    chart.plot()
    pass


if __name__ == '__main__':
    main()
