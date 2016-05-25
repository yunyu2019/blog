#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:oxygen
# http://www.pythonchallenge.com/pc/def/channel.zip 得到第五关的所有参数
import re
import os
import zipfile

zip_path='pc06-channel.zip'
zfile=zipfile.ZipFile(zip_path)
"""
#方法一
def readzip(zfile,ids):
    file_path='%s.txt' % ids
    cont=zfile.read(file_path)
    comment=zfile.getinfo(file_path).comment
    print comment,
    next_id=re.findall('(\d+)',cont)
    if next_id:
        leng=len(next_id)
        readzip(zfile,next_id[leng-1])
    
readzip(zfile,'90052')
"""
#方法二
number='90052'
comments=''
while number:
    file_path='%s.txt' % number
    cont=zfile.read(file_path)
    comment=zfile.getinfo(file_path).comment
    comments+=comment
    next_id=re.findall('(\d+)',cont)
    if next_id:
        leng=len(next_id)
        number=next_id[leng-1]
    else:
        break
    print number
print comments
print number
"""
图片中出现了hockey的字符
在地址栏输入hockey后出现提示，要输入oxygen
"""
