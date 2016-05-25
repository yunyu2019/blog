#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:序列与反序列化pickle
import pickle
import pprint
import urllib2

urls='http://www.pythonchallenge.com/pc/def/banner.p'
fp=urllib2.urlopen(urls)
cont=pickle.load(fp)

"""
#方法一
def makestring(line):
    s=''
    for char,num in line:
        s+=char*num
    return s

for line in cont:
    s=makestring(line)
    print s
"""

#方法二简化代码
print '\n'.join([''.join([p[0] * p[1] for p in row]) for row in cont])