#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/5808.html
import Image
img=Image.open('cave.jpg')
w,h=img.size
ls=[]
for x in range(w):
    for y in range(h):
        if (x+y)%2 ==1:
           img.putpixel((x,y),0)
img.save('cave2.jpg')