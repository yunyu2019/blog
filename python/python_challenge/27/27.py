#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-20 17:01:47
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/speedboat.html

import bz2
import Image
from keyword import iskeyword

img=Image.open('zigzag.gif')
data=list(img.getdata())
colors=img.getpalette()[::3]
data2=[colors[i] for i in data]
data1=data[1:]+[data[0]]
l=[x for x,y in zip(data1,data2) if x!=y]
s=''.join(map(chr,l))
cont=bz2.decompress(s).split()
n=set([x for x in cont if not iskeyword(x)])
print n #set(['../ring/bell.html', 'switch', 'repeat'])


