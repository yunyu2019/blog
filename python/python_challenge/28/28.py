#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 16:14:22
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : www.pythonchallenge.com/pc/ring/bell.html

import Image
img=Image.open('bell.png')
img.load()
r,g,b=img.split()
data=list(g.getdata())
l=zip(data[::2],data[1::2])
l1=[abs(odd-even) for odd,even in l if abs(odd-even)!=42]
s=''.join(map(chr,l1))
print s #whodunnit().split()[0] ?
"""
whodunnit().split()[0] ? 读出来hudownit==>Guido van Rossum==>guido
"""