#!/usr/bin/python
# -*- coding: utf-8 -*-
file_path='pc02-data.txt'
with open(file_path,'r') as fp:
    cont=fp.read()
ls=[char for char in cont if char.isalpha()]
s=''.join(ls)
ls='ocr'
old_url='http://www.pythonchallenge.com/pc/def/ocr.html'
new_url=old_url.replace(ls,s)
print new_url