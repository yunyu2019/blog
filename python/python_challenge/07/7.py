#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
import re
from PIL import Image

file_path='oxygen.png'
image=Image.open(file_path)
w,h=image.size
grey_list=[image.getpixel((x,47))[0] for x in range(1,610,7)]
s=''.join(chr(x) for x in grey_list)
"""
result:smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]
"""
ls=re.findall('\[.+\]',s)
ls=eval(ls[0])
result=map(chr,ls)
res=''.join(result)
old_url='http://www.pythonchallenge.com/pc/def/oxygen.html'
new_url=old_url.replace('oxygen',res)
print new_url

