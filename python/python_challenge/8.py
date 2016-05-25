#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:bz2压缩解压模块 repr()以字符串的形式显示一个python对象
import bz2
un='BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
pw='BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'
new_un=bz2.decompress(un)
new_pw=bz2.decompress(pw)
print new_un
print new_pw