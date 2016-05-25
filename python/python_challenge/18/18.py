#/usr/bin/python
#-*- coding: utf-8 -*-
#note:
#http://www.pythonchallenge.com/pc/return/balloons.html
"""
bright==>http://www.pythonchallenge.com/pc/return/bright.html==>http://www.pythonchallenge.com/pc/return/brightness.html==>deltas.gz
"""
import gzip
import difflib
import binascii

text=gzip.open('deltas.gz').read()
lines=text.splitlines()
part1=[l[0:53] for l in lines]
part2=[l[56:] for l in lines]
d=list(difflib.Differ().compare(part1,part2))
pngs=zip(['same.png','plus.png','minus.png'],[''.join(l[1:] for l in d if l[0]==c) for c in " +-"])
for filename,cont in pngs:
    hexstr=cont.replace(' ','')
    data=binascii.unhexlify(hexstr) #二进制转换成ascii字符串形式
    fp=open(filename,'wb')
    fp.write(data)
    fp.close()
#www.pythonchallenge.com/pc/hex/bin.html==>user:butter,password:fly