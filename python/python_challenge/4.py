#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import time
import urllib2

ids='12345'
i=0
while i<400:
    i+=1
    urls='http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%s' % ids
    cont=urllib2.urlopen(urls).read()
    if cont=='':
        break
    print 'times:%s id:%s content:%s' % (i,ids,cont)
    if i==86:
        ids=int(ids)
        ids=str(ids/2)
    else:
        if re.findall('(\d+)',cont):
            s=re.findall('(\d+)',cont)
            length=len(s)
            ids=s[length-1]
        else:
            break
print cont
old_url='http://www.pythonchallenge.com/pc/def/linkedlist.php'
new_url=old_url.replace('linkedlist.php',cont)