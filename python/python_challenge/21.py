#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-12 10:53:31
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/idiot2.html

import bz2
import zlib
import zipfile
import binascii

def readascii(s):
     return s if s.isalpha() or s.isdigit() else ''

def show(data,length=24):
    s=' '.join(map(binascii.b2a_hex,data[:length]))
    s1=' '.join(map(readascii,data[:length]))
    print len(data)
    print s
    print s1
    

zp=zipfile.ZipFile('./20/unreal.zip')
passwd='invader'[::-1]
zp.setpassword(passwd)
data=zlib.decompress(zp.read('package.pack'))
logs=[]
while True:
    if data[:2]=='\x78\x9c':
        data=zlib.decompress(data)
        logs.append(' ') #z
    elif data[:2]=='BZ':
        data=bz2.BZ2Decompressor().decompress(data)
        logs.append('#') #b
    elif data[-2:]=='\x9c\x78':
        data=zlib.decompress(data[::-1])
        logs.append('\n') #Z
    else:
        break
show(data) #s g o l  r u o y  t a  k o o l==>look at your logs
print ''.join(logs)