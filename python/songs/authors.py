#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-07 14:48:29
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : 抓取单页的作者信息

import re
import json
import codecs
import urlparse
import requests
from bs4 import BeautifulSoup
from pypinyin import lazy_pinyin

urls="http://so.gushiwen.org/author_858.aspx"
req=requests.get(urls)
s=urlparse.urlparse(urls)
author_url=s.path
cont=req.content
item=dict()
soup=BeautifulSoup(cont,'lxml')
son1 =soup.find_all('div',attrs={'class':'son1'})
author=son1[1].findChild('h1').get_text()
son2=soup.find_all('div',attrs={'class':'son2'})
img=son2[1].findChild('img')
author_desc=son2[1].get_text()
item['author']=author
item['faceimg']=img['src'] if img else ''
item['author_url']=author_url
author_id=0
if author_url!='':
	m=re.search('(\d+)',author_url)
	author_id=m.group(1)
item['pinyin']=''
if item['author']:
	author_name=lazy_pinyin(item['author'])
	item['pinyin']=''.join(author_name)
item['author_url']=author_url
item['author_id']=author_id
item['dynasty']=''
item['author_desc']=author_desc.strip()
relation_urls=[]
res1=soup.find_all('div',attrs={'class':'son5'})
for v in res1:
	a=v.find('p').findChild('a')
	relation_urls.append(a['href'])
item['relation_url']=relation_urls
for v in res1:
	a=v.find('p').findChild('a')
	item['view_url']=a['href']
	req2=requests.get('http://so.gushiwen.org'+item['view_url'])
	cont2=req2.content
	soup2=BeautifulSoup(cont2,'lxml')
	son1 =soup2.find_all('div',attrs={'class':'son1'})
	title=son1[1].findChild('h1').get_text()
	strs=soup2.find('div',attrs={"class":"shangxicont"})
	editor=strs.find('p').get_text()
	rule=re.compile('<div class="shangxicont".*?</p>?(.*)?.*<p style=".*?color:#919090.*?',re.S)
	m=re.search(rule,cont2)
	content=m.group(1).strip() if m else ''
	item['title']=title
	item['editor']=editor
	item['content']=content
	fp= codecs.open('datas.json', 'a', encoding='utf-8')
	line = json.dumps(item, ensure_ascii=True) + "\n"
	fp.write(line)

fp.close()

