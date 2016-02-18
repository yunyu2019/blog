#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import urllib2
import os
import urlparse
import MySQLdb
import time
import codecs
from pypinyin import lazy_pinyin

class Tool:
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;|&middot;|[-|.]{3,}')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

def bra(s):
    rule=re.compile('[6-9]{1}[0-9]{1}[a-g|A-G]?',re.I)
    flag=re.match(rule,s)
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
    else:
        return s

def gettime():
    curr_time=time.localtime()
    curr_time=time.strftime('%Y-%m-%d %H:%M:%S',curr_time)
    return curr_time

page=779
list_url='https://mm.taobao.com/json/request_top_list.htm?page='+str(page)
header={
            'Host':'mm.taobao.com',
            'Cookie':'thw=cn; miid=7592320213040609111; cna=1u4ZD8yNDC8CAcpqqeiyKnT0; isg=0830773A8D1358D2A801D5B0D3BFE2E2; uc3=nk2=txBJoUSGvqg%3D&id2=UU23C%2B9%2BZQMNjA%3D%3D&vt3=F8dASccesVq5kGzOoP4%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu4E91%5Cu8BED2019; tracknick=%5Cu4E91%5Cu8BED2019; _cc_=VT5L2FSpdA%3D%3D; tg=0; mt=ci=0_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; CNZZDATA30063598=cnzz_eid%3D55660832-1454057992-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454057992; CNZZDATA30064598=cnzz_eid%3D620701788-1454056446-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454056661; CNZZDATA30063600=cnzz_eid%3D880614795-1454056379-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454060018; l=Aj09zKxfGs7gtZD/TZQ/7wWezZM3s3Ej; v=0; _tb_token_=DlV8upUHUziAwx3; JSESSIONID=1C6390961BDC114F40264472BEDFF54C; uc1=cookie14=UoWyiqrPiMUB%2Fw%3D%3D; cookie2=1cf6800e7b26483ec5ccc10658927160; t=cf614df5632b038d72bf347e2a24d6b3',
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0'
}
req=urllib2.Request(list_url,headers=header)
try:
    html=urllib2.urlopen(req).read().decode('gbk')
    rule=re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<em><strong>(.*?)</strong>.*?</em>.*?<img data-ks-lazyload="(.*?)".*?/>.*?class="popularity".*?<dd>.*?(\d+).*?</dd>.*?class="info-detail".*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<p class="description">(.*?)</p>?',re.S)
    contents=re.findall(rule,html)
    content=contents[1]
    tool=Tool()
    sname=content[3]
    if sname=='':
        sname=profiles[0]
    upin=lazy_pinyin(sname)
    name=''
    for uname in upin:
        name+=uname
    
    profile_url='https:'+content[2]
    result=urlparse.urlparse(profile_url)
    params=urlparse.parse_qs(result.query)
    profile_url='https://mm.taobao.com/self/info/model_info_show.htm?user_id='+params['user_id'][0]
    header1={
       'Host':'mm.taobao.com',
       'cookie':'swfstore=294769; thw=cn; miid=7592320213040609111; cna=1u4ZD8yNDC8CAcpqqeiyKnT0; isg=0830773A8D1358D2A801D5B0D3BFE2E2; uc3=nk2=txBJoUSGvqg%3D&id2=UU23C%2B9%2BZQMNjA%3D%3D&vt3=F8dASccesVq5kGzOoP4%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu4E91%5Cu8BED2019; tracknick=%5Cu4E91%5Cu8BED2019; _cc_=VT5L2FSpdA%3D%3D; tg=0; mt=ci=0_1; CNZZDATA30063598=cnzz_eid%3D55660832-1454057992-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454294534; v=0; _tb_token_=te7941FAFzKUtf7; CNZZDATA30064598=cnzz_eid%3D620701788-1454056446-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454376870; CNZZDATA30063600=cnzz_eid%3D880614795-1454056379-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454375141; l=Ah4ep2qW6duvGBPi2rFs4ZnD7r5g3-JZ; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=CBB46AA5B26B61A77FE3E8F34A9E8801; uc1=cookie14=UoWyiqv3bfJSJA%3D%3D; cookie2=15fca6d3c3578cb62acba0a81d2504fb; t=cf614df5632b038d72bf347e2a24d6b3',
       'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0'          
    }
    req1=urllib2.Request(profile_url,headers=header1)
    html1=urllib2.urlopen(req1).read().decode('gbk')
    rule=re.compile('<ul class="mm-p-info-cell clearfix".*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<div class="mm-p-info mm-p-experience-info">.*?<p>(.*?)</p>.*?class="mm-p-modelCard".*?<img src="(.*?)".*?/>?',re.S)
    profiles=re.findall(rule,html1)
    profile=profiles[0]
    bras=bra(profile[10])
    
    conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="taobao",charset="utf8")
    cursor = conn.cursor()
    try:
        sql="insert into `user` (`name`,`age`,`profile_url`,`faceimg`,`tags`,`descp`,`city`,`imgnums`,`integral`,`fans`,`signnum`,`rates`,`model_img`,`big_img`,`life_img`,`pinyin`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        n=cursor.execute(sql,(content[3],content[4],'https:'+content[0],'https:'+content[1],content[6],content[14],content[5],content[12],content[9],content[7],content[13],content[11],'','https:'+content[8],'https:'+profile[13],name))
        userid=conn.insert_id()
        school=tool.replace(profile[5])
        borthday=tool.replace(profile[1])
        exprince=tool.replace(profile[12])
        blood=profile[4]
        sql1="insert into `profile` (`user_id`,`nicename`,`borthday`,`blood`,`school`,`style`,`height`,`weight`,`solid`,`bar`,`shoes`,`exprince`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        n=cursor.execute(sql1,(str(userid),profile[0],borthday,blood,school,profile[6],profile[7],profile[8],profile[9],bras,profile[11],exprince))
        #conn.commit()
    except MySQLdb.Error,e:
        #conn.rollback()
        curr_time=gettime()
        fp=codecs.open('e:/taobao/error.txt','a','utf-8')
        fp.write(curr_time+u' '+str(page)+u' 页 '+sname+u'错误: '+str(e)+'\n')
        fp.close()
    
    abpath='e:/taobao/'+str(page)+'/'+name
    if not os.path.exists(abpath):
        os.makedirs(abpath)
    print u'开始保存 %s 详细信息' % name
    fp=codecs.open(abpath+'/profile.txt','wb','utf-8')
    for v in content:
        temp=v.replace('\t','')
        temp=v.replace('\n','')
        fp.write(temp+'\n')
    for j in profile:
        temp=j.replace('\t','')
        temp=j.replace('\n','')
        fp.write(temp+'\n')
    fp.close()
except urllib2.HttpError,e:
    errors=''
    if hasattr(e,'reason'):
        errors=str(e.reason)
    elif hasattr(e,'code'):
        errors='error code:'+e.code+' message:'+e.reade()
    curr_time=gettime()
    fp=codecs.open('e:/taobao/error.log','a','utf-8')
    fp.write(curr_time+' '+str(page)+u' 错误:'+errors+'\n')
    fp.close()
    
except urllib2.URLError,e:
    errors=''
    if hasattr(e,'reason'):
        errors=str(e.reason)
    elif hasattr(e,'code'):
        errors='error code:'+e.code+' message:'+e.reade()
    curr_time=gettime()
    fp=codecs.open('e:/taobao/error.log','a','utf-8')
    fp.write(curr_time+' '+str(page)+u' 错误: '+errors+'\n')
    fp.close()
else:
    pass