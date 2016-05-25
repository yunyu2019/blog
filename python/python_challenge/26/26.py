#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-20 16:09:42
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/decent.html

"""
From: leopold.moz@pythonchallenge.com
Subject: Re: sorry
Date: 2007-05-17 15:37:07 BDT
Never mind that.
Have you found my broken zip?
md5: bbb8b499a0eef99b52c7f13f4e78c24b
Can you believe what one mistake can lead to?
"""

from hashlib import md5

def repair(data,md5str):
    nums=len(data)
    for i in range(nums):
        bake=data[i]
        for byte in range(256):
            data[i]=byte
            if md5(data).hexdigest()==md5str:
                print '错误的字节位置是:%s' % i
                return True
        data[i]=bake
    return False

md5str='bbb8b499a0eef99b52c7f13f4e78c24b'
fp=open('mybroken.zip','rb')
data=bytearray(fp.read())
fp.close()
if repair(data,md5str):
    fp=open('repair.zip','wb')
    fp.write(data)
    fp.close()
    print '修复完毕'
    

