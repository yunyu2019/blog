#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
file_path='pc03-data.txt'
with open(file_path,'r') as fp:
    cont=fp.read()
rule=re.compile('[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]')
s=re.findall(rule,cont)
s1=''.join(s)+'.php'
old_url='http://www.pythonchallenge.com/pc/def/ocr.html'
new_url=old_url.replace('ocr.html',s1)
print new_url