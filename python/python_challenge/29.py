#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-23 17:08:53
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/ring/guido.html

import bz2
import requests

req=requests.get('http://www.pythonchallenge.com/pc/ring/guido.html',auth=('repeat','switch'))
"""
cont=req.content
print cont.splitlines()[12:]
"""
l=list(req.iter_lines())[12:]

l1=[len(i) for i in l]
s=''.join(map(chr,l1))
cont=bz2.decompress(s)
print cont #Isn't it clear? I am yankeedoodle!
#picture:whoisit.png==>yankeedoodle