#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/bull.html
"""
#方法一
import re
def getNext(strs):
    return ''.join(str(len(match.group(0))) + match.group(1) for match in re.finditer(r'(\d)\1*',strs))
strs='111221'
length=5
while length<31:
    strs=getNext(strs)
    length+=1
print len(strs)
"""
def getNext(strs):
    if strs=='':
        return ''
    curnum=strs[0]
    num=1
    nextstr=''
    for x in strs[1:]:
        if x == curnum:
            num+=1
        else:
            nextstr+=str(num)+curnum
            curnum=x
            num=1
    nextstr+=str(num)+curnum
    return nextstr
strs='111221'
length=5
while length<70:
    strs=getNext(strs)
    length+=1
print len(strs)