#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-10 16:23:57
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : 反转图像的色彩

import Image
def unshiftColor(color):
	r,g,b=color
	return 255-r,255-g,255-b

img=Image.open('map.jpg')
data=map(unshiftColor,img.getdata())
img.putdata(data)
img.save('nmap1.jpg')

