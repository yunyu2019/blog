#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import MySQLdb

conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="taobao",charset="utf8")
cursor = conn.cursor()
def getbar(upbar,num):
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
    if upbar!='':
        bar=str(bar)+upbar.upper()
    return bar
def transforBar():
    sql='select id,bar from profile where id>9179'
    cursor.execute(sql)
    results=cursor.fetchall()
    sum=0
    wids=[]
    duids=[]
    for result in results:
        rule=re.compile('^[6-7]{1}[0-9]{1}[a-g]?',re.I)
        rule1=re.compile('^[a-g]?[6-9]{1}[0-9]{1}',re.I)
        rule2=re.compile('^[3-4]{1}[0-9]{1}[a-g]')
        if re.match(rule,result[1]):
            m=re.search('^(\d+)(\w?)',result[1])
            num=m.group(1)
            num=int(num)
            upbar=m.group(2)
            bar=getbar(upbar,num)
            sql1='update profile set bar=%s where id=%s'
            cursor.execute(sql1,(bar,result[0]))
            sum+=1;
            wids.append(result[0])  
        elif re.match(rule1,result[1]):
            m=re.search('(\w?)(\d+)',result[1])
            num=m.group(2)
            num=int(num)
            upbar=m.group(1)
            bar=getbar(upbar,num)
            sql1='update profile set bar=%s where id=%s'
            cursor.execute(sql1,(bar,result[0]))
            sum+=1;
            wids.append(result[0])
        elif re.match(rule2,result[1]):
            m=re.search('^(\d+)(\w?)',result[1])
            bar=m.group(1)
            upbar=m.group(2)
            bar=bar+upbar.upper()
            sql1='update profile set bar=%s where id=%s'
            cursor.execute(sql1,(bar,result[0]))
            sum+=1;
            duids.append(result[0])
        else:
            continue
    print u'共计更新记录%s条' % sum
    print duids
    print wids
transforBar()