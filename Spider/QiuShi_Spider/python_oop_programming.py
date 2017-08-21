#!/usr/bin/env python
# encoding: utf-8

# @file: python_oop_programming.py
# @time: 2017/7/17 15:20
# @author: FunnyWu
# @license: Apache Licence 
# @contact: agiot1026@163.com
# @Software: PyCharm


class Phone(object):
    name = ''
    version = ''

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __hash__(self):
        return super(Phone, self).__hash__()

    def print_class_property(self):
        print 'name:' + self.name + '\tversion:' + str(self.version)


class Student(object):
    name = ''
    sex = ''
    native_place = ''  # 籍贯
    total_score = 0

    def __init__(self, name, sex, native_place, total_score=0):
        self.name = name
        self.native_place = native_place
        self.sex = sex
        self.total_score = total_score

    def print_student_info(self):
        print (u'姓名:' + self.name
               + u'\t性别:' + self.sex
               + u'\t籍贯:' + self.native_place
               + u'总成绩:' + str(self.total_score))


if __name__ == '__main__':
    # phone = Phone('vivo X5 Pro D', 1.0)
    # phone.print_class_property()
    student = Student(u'FunnyWu', u'男', u'重庆开县', 100)
    student.print_student_info()
