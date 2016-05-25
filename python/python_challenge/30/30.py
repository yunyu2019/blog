#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 17:50:46
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : www.pythonchallenge.com/pc/ring/yankeedoodle.html

import re
import Image

cont=open('yankeedoodle.csv','r').read()
l=re.findall('(0.\d+)',cont)

data=[int(255*float(x)) for x in l]
img=Image.new('P',(53,139))
img.putdata(data)
img=img.transpose(Image.ROTATE_90)
img=img.transpose(Image.FLIP_TOP_BOTTOM)
img.save('output.png')

l1=zip(l[0::3],l[1::3],l[2::3])
l2=[int(x[0][5]+x[1][5]+x[2][6]) for x in l1]
print ''.join(map(chr,l2))
"""
So, you found the hidden message.
There is lots of room here for a long message, but we only need very little space to say "look at grandpa", so the rest is just garbage. 
"""
