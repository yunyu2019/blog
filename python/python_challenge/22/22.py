#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-12 13:37:47
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/copper.html

import Image

"""
fp=open('white.gif','rb')
data=fp.read()
fp.close()
new_data=data[:37]+'\xff\xff\xff'+data[40:]
fp=open('white1.gif','wb')
fp.write(new_data)
fp.close()
"""

def mymovements():
	im=Image.open('white.gif')
	ox,oy=100,100
	frame=0
	while True:
		try:
			im.seek(frame)
		except:
			break
		x,y=im.getbbox()[:2]
		dx,dy=x-ox,y-oy
		yield (dx,dy)
		frame+=1

img=Image.new('P',(400,100),0)
white=255
x,y=0,50
for movement in mymovements():
	if movement==(0,0):
		x=x+50
		y=50
	else:
		dx,dy=movement
		x,y=x+dx,y+dy
	img.putpixel((x,y),white)

img.save('white2.png')

