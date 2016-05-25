#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-17 16:36:18
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/lake.html

import os
import wave
import time
import Image
import requests

def download(urls):  
    filename=os.path.basename(urls)
    try:
        req=requests.get(urls,auth=('butter','fly'))
        fp=open(filename,'wb')
        fp.write(req.content)
        fp.close()
        print 'download:%s' % filename
    except:
        print 'fail download:%s' % filename


def getdatas(files):
    fp=open(files,'rb')
    data=fp.read()[44:]
    fp.close()
    img=Image.new('RGB',(60,60))
    img.fromstring(data)
    return img
"""
for i in range(1,26):
    urls='http://www.pythonchallenge.com/pc/hex/lake%s.wav' % i
    download(urls)
    time.sleep(1)
"""
img=Image.new('RGB',(300,300))
for i in range(25):
    y,x=divmod(i,5)
    files='lake{0}.wav'.format(i+1)
    pices=getdatas(files)
    img.paste(pices,(x*60,y*60))
img.save('lake.jpg')