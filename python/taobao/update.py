#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import MySQLdb

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="taobao",charset="utf8")
cursor = conn.cursor()
sql='select id,bar from profile where id>5565'

cursor.execute(sql)
results=cursor.fetchall()
for result in results:
    rule=re.compile('[6-9]{1}[0-9]{1}[a-g|A-G]?',re.I)
    flag=re.match(rule,result[1])
    if flag:
        m=re.search('(\d+)(\w?)',result[1])
        num=m.group(1)
        num=int(num)
        bar=30
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
        upbar=m.group(2)
        if upbar!='':
            bar=str(bar)+upbar.upper()
        sql1='update profile set bar=%s where id=%s'
        cursor.execute(sql1,(bar,result[0]))
    else:
        continue