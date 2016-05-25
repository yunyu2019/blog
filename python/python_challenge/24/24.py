#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-13 16:24:29
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/ambiguity.html

import Image
import ImageDraw

def getPath(imgsrc,wall):
    path = []
    wholepath = []
    dire = [(1,0),(0,1),(-1,0),(0,-1)]
    
    img = Image.open(imgsrc)
    w,h=img.size
    
    for i in range(h):
        if img.getpixel((i,0))[0]==0:
            pos = (i,0)
        if img.getpixel((i,w-1))[0]==0:
            endpos = (i,w-1)
           
    while pos!=endpos:
        img.putpixel(pos, wall)
        flag = 0
        newpos = pos
        for i in dire:
            try:
                pp = (pos[0]+i[0],pos[1]+i[1])
                if img.getpixel(pp)!=wall:
                    flag+=1
                    newpos = pp
            except:
                pass
        if flag==0:
            if path == []:
                path = wholepath.pop()
                continue
            pos = path[0]
            path = []
        elif flag>1:
            wholepath.append(path)
            path = [pos]
            pos = newpos
        else:
            path.append(pos)
            pos = newpos
    else:       
         path.append(pos)
         wholepath.append(path)
    return wholepath

imgsrc='maze.png'
wall=(255,)*4
wholepath=getPath(imgsrc,wall)
img=Image.open(imgsrc)
img1 = Image.new('RGBA',img.size,'black')
newimg = ImageDraw.Draw(img1)
data = [(img.getpixel(k)[0],img1.putpixel(k, wall)) for i in wholepath for k in i]
s=''.join(map(chr,[i[0] for i in data[1::2]]))
out = open('out.zip','wb')
out.write(s)
out.close()
img1.save('out.png')