#!/usr/bin/env python
# encoding: utf-8

# @file: python_re.py
# @time: 2017/7/18 10:16
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm

import re

filename = "output_1981.10.21.txt.12."

result = re.search(r'[\d\.]+', filename)
if result:
    print result.group()

str = "My age is 18,but I love python"

result = re.findall(r'[A-Z]', str)

print ''.join(result)
