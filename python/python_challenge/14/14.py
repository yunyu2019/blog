#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/italy.html
import Image
img=Image.open('wire.png')
canvas=Image.new('RGB',(100,100),0)
dirs =[(1,0),(0,1),(-1,0),(0,-1)] #控制方向
x,y,z = -1,0,0
for i in range(200):
    d = dirs[i % 4]
    for j in range(100 - (i + 1) // 2):
        x += d[0]
        y += d[1]
        canvas.putpixel((x,y),img.getpixel((z,0)))
        z += 1
canvas.save('2.png')
"""
打开www.pythonchallenge.com/pc/return/cat.html
and its name is <b>uzi</b>. you'll hear from him later.
"""