#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/mozart.html
import Image
img=Image.open('mozart.gif')
w,h=img.size
magenta = 195
for y in range(h):
	rect=0,y,w,y+1
	row=img.crop(rect)
	data=list(row.getdata())
	p=data.index(magenta) #找到195颜色的元素的位置
	row=row.offset(-p) #这里实现的平移是将左侧多出的部分移到了右侧
	img.paste(row,rect)
img.save('shift.png')