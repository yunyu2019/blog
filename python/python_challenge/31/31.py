#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 18:29:57
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/ring/grandpa.html
#user:'kohsamui'
#password:'thailand'

import Image
import requests

"""
req=requests.get('http://www.pythonchallenge.com/pc/rock/mandelbrot.gif',auth=('kohsamui','thailand'))
fp=open('mandelbrot.gif','wb')
fp.write(req.content)
fp.close()
"""

imgbase = Image.open('mandelbrot.gif')
img = imgbase.copy()
w,h=imgbase.size
left = 0.34
top = 0.57+0.027
width = 0.036
height = 0.027
nums = 128
diff = []
for j in range(h):
    for i in range(w):
        point0 = complex(left + i*width/w, top - (1+j)*height/h)
        point = 0+0j 
        for k in range(nums):
            point = point **2 + point0
            if point.imag**2+point.real**2>4:
                break
        img.putpixel((i,j),k)
        s=imgbase.getpixel((i,j))
        if k!=s:
            diff.append(k - s)
img.save('output.png')
img2 = Image.new('1',(23,73))
data=[i<0 for i in diff]
img2.putdata(data)
img2.save('output1.png')
#Arecibo message