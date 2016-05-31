#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-31 16:17:59
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import re

def filterHtml(strings):
	compiles=re.compile(r'<[^>]+>',re.S)
	s=re.sub(compiles,'',strings)
	return s.strip()

def bar(s):
    rule=re.compile('^[6-9]{1}[0-9]{1}[a-g]?',re.I)
    rule1=re.compile('^[a-g]?[6-9]{1}[0-9]{1}',re.I)
    rule2=re.compile('^[3-4]{1}[0-9]{1}[a-g]')
    flag=False
    if re.match(rule,s):
        m=re.search('(\d+)(\w?)',s)
        num=m.group(1)
        upbar=m.group(2)
        flag=True
    elif re.match(rule1,s):
        m=re.search('(\w?)(\d+)',s)
        num=m.group(2)
        upbar=m.group(1)
        flag=True
    elif re.match(rule2,s):
        m=re.search('^(\d+)(\w?)',s)
        num=m.group(1)
        upbar=m.group(2)
        flag=True
    if flag:
        num=int(num)
        bar=30
        if num<60:
            bar=num
        if num>=68 and num<=72:
            bar=32
        elif num>=73 and num<=77:
            bar=34
        elif num>=78 and num<=82:
            bar=36
        elif num>=83 and num<=87:
            bar=38
        elif num>=88 and num<=92:
            bar=40  
        if upbar!='':
            bar=str(bar)+upbar.upper()
        return bar
    else:
        s=s.replace('----','')
        return s

