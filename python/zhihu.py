#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-02 15:25:40
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : 模拟登陆知乎

import re
import copy
import requests
from bs4 import BeautifulSoup

def filterNumber(s):
	m=re.search('(\d+)',s)
	num=m.group(1) if m else 0
	return num

headers={
	'Host':'www.zhihu.com',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
}
req=requests.get('https://www.zhihu.com/#signin',headers=headers)
cont=req.content
#soup=BeautifulSoup(cont,'lxml')
soup=BeautifulSoup(cont,'html.parser')
xsrf=soup.find('input',attrs={"name":"_xsrf"})
headers1=copy.copy(headers)
headers1['Referer']='https://www.zhihu.com/'
headers1['X-Xsrftoken']=xsrf['value']
datas={
    '_xsrf':xsrf['value'],
    'email':'yunyu2010@yeah.net',
    'password':'*****',
    'remember_me':'true'
}
req1=requests.post('https://www.zhihu.com/login/email',data=datas,headers=headers1)

req2=requests.get('https://www.zhihu.com/question/following',headers=headers,cookies=req1.cookies)
follows=req2.content
soup1=BeautifulSoup(follows,'html.parser')
topics=soup1.find_all('div',attrs={'class':'zm-profile-section-item'})
items=list()
for i in topics:
	item=dict()
	a=i.find('a',attrs={'class':'question_link'})
	nums=i.find('div',attrs={'class':'zm-profile-vote-num'}).get_text()
	url=a.attrs['href']
	title=a.text.encode('utf-8').strip()
	bulls=i.find_all('span',attrs={'class':'zg-bull'})
	answer=0
	follow=0
	if len(bulls)>1:
		answer=filterNumber(bulls[0].next_sibling.encode('utf-8'))
		follow=filterNumber(bulls[1].next_sibling.encode('utf-8'))
	item['title']=title
	item['url']=url
	item['scan']=nums
	item['follow']=follow
	item['answer']=answer
	items.append(item)

for item in items:
	print 'topic:{title} link:https://www.zhihu.com{url} follow:{follow} scan:{scan} join:{answer}'.format(**item)

	




