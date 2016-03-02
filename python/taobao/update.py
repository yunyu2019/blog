#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import os
import MySQLdb
import urllib2
import time
import logging
import imghdr

logpath='e:/taobao/logs'
errorFormatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
infoFormatter=logging.Formatter('%(asctime)s %(message)s')
curr_time=time.localtime()
currDate=time.strftime('%Y-%m-%d',curr_time)
infoName=logpath+r'/info_%s.log' % currDate
errorName=logpath+r'/error_%s.log' % currDate
errorLogger=logging.getLogger('error')
infoLogger=logging.getLogger('info')

errorHandler=logging.FileHandler(errorName,mode='a',encoding='utf-8')
errorLogger.setLevel(logging.ERROR)
errorHandler.setFormatter(errorFormatter)
errorLogger.addHandler(errorHandler)

infoLogger.setLevel(logging.INFO)
infoHandler=logging.FileHandler(infoName,mode='a',encoding='utf-8')
infoHandler.setFormatter(infoFormatter)
infoLogger.addHandler(infoHandler)

def saveimg(img_url,subdir,descp):
    """保存图片"""
    fn=img_url.split('/')
    abpath='e:/taobao/images/'+str(subdir)
    if not os.path.exists(abpath):
        os.makedirs(abpath)
    try:
        data=urllib2.urlopen(img_url,timeout=20).read()
        file_path=abpath+'/'+fn[-1]
        f=open(abpath+'/'+fn[-1],'wb')
        f.write(data)
        f.close()
        rule=re.compile('(.*)\.(jpg|jpeg|png|gif)',re.I)
        if re.match(rule,file_path):
           pass
        else:
           imgType = imghdr.what(file_path)
           dfile=file_path+'.'+imgType
           os.rename(file_path,dfile) 
        msg='save id:%s %s image ===========  ok' % (subdir,descp)
        infoLogger.info(msg)
    except urllib2.HTTPError,e:
        errors=''
        if hasattr(e,'reason'):
            errors=str(e.reason)
        elif hasattr(e,'code'):
            errors='error code:'+e.code+' message:'+e.reade()
        print u'save %s image  error ==== OK' % descp
        msg=u'保存图片:'+img_url+u'失败:'+errors
        errorLogger.error(msg)
    except urllib2.URLError,e:
        errors=''
        if hasattr(e,'reason'):
            errors=str(e.reason)
        elif hasattr(e,'code'):
            errors='error code:'+e.code+' message:'+e.reade()
        msg=u'保存图片:'+img_url+u'失败:'+errors
        errorLogger.error(msg)
    else:
        pass



conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="taobao",charset="utf8")
cursor = conn.cursor()
sql='select id,life_img,big_img from user where id=1067'
cursor.execute(sql)
results=cursor.fetchall()
ids=[]

for result in results:
    compiles=re.compile('(?:https|http)://(.*)\.(jpg|jpeg|png|gif)',re.I)
    flag=0
    if re.match(compiles,result[1]):
        continue
    else:
        flag=1

    if re.match(compiles,result[2]):
        continue
    else:
        flag=2

    if flag>0:
        ids.append(result[0])
    if flag==1:
        saveimg(result[1],result[0],'life img')
    if flag==2:
        saveimg(result[2],result[0],'big img')
    time.sleep(1)    
print ids
        
"""
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
"""