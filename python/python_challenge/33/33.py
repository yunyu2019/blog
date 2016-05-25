#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-25 16:49:18
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : www.pythonchallenge.com/pc/rock/beer.html

import os
import math
import Image
import requests

def downfile(url):
    req=requests.get(url,auth=('kohsamui','thailand'))
    filename=os.path.basename(url)
    fp=open(filename,'wb')
    fp.write(req.content)
    fp.close()
    return filename

filename=downfile('http://www.pythonchallenge.com/pc/rock/beer2.png')
img=Image.open(filename)
data=img.getdata()
colors=img.getcolors()

m=1
length=len(colors)
for i in range(length-1,-1,-2):
    s = []
    t = []
    for j in data:
        if j!=colors[i][1] and j!=colors[i-1][1]:
            s.append(j)
            t.append(0)
        else:
            if j==colors[i][1]:
                t.append(1)
            else:
                t.append(0)
    data = s
    n = int(math.sqrt(len(t)))
    new = Image.new('1',(n,n))
    new.putdata(t)
    new.save('beers/beer%d.png' % m)
    m+=1

#fair and square==>gremlins