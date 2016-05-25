#/usr/bin/python
#-*- coding: utf-8 -*-
#note:
#http://www.pythonchallenge.com/pc/return/romance.html
#图片中左下角是谜题四的题图，与第四关有关联

import re
import bz2
import requests
import xmlrpclib
from  urllib import unquote_plus
ids='12345'
i=0
ls=''
while i<400:
    i+=1
    urls='http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=%s' % ids
    req=requests.get(urls)
    cont=req.text
    info=req.cookies.get('info')
    ls+=info
    print 'times:%s id:%s content:%s cookies:%s' % (i,ids,cont,info)
    if re.findall('(\d+)',cont):
        s=re.findall('(\d+)',cont)
        length=len(s)
        ids=s[length-1]
    else:
        break
"""
ls='BZh91AY%26SY%94%3A%E2I%00%00%21%19%80P%81%11%00%AFg%9E%A0+%00hE%3DM%B5%23%D0%D4%D1%E2%8D%06%A9%FA%26S%D4%D3%21%A1%EAi7h%9B%9A%2B%BF%60%22%C5WX%E1%ADL%80%E8V%3C%C6%A8%DBH%2632%18%A8x%01%08%21%8DS%0B%C8%AF%96KO%CA2%B0%F1%BD%1Du%A0%86%05%92s%B0%92%C4Bc%F1w%24S%85%09%09C%AE%24%90'
"""
print bz2.decompress(unquote_plus(ls)) 
#result:is it the 26th already? call his father and inform him that "the flowers are on their way". he'll understand.

phonebook=xmlrpclib.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
call=phonebook.phone('Leopold') #Leopold is Mozart's father
res=call[4:].lower() #violin ==> http://www.pythonchallenge.com/pc/stuff/violin.php
data={'info':'the flowers are on their way'}
req=requests.get('http://www.pythonchallenge.com/pc/stuff/violin.php',cookies=data)
cont=req.text
print cont #result:oh well, don't you dare to forget the balloons.