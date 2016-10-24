#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-13 15:54:38
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import os
import re
import json
import copy
import time
import codecs
import requests
from lxml import etree
from bs4 import BeautifulSoup

class Follows(object):
	"""docstring for ClassName"""
	def __init__(self):
		self.login_url='https://www.zhihu.com/#signin'
		self.login_uri='https://www.zhihu.com/login/email'
		self.follow_url='https://www.zhihu.com/people/excited-vczh/followees'
		self.headers={
		    'Host':'www.zhihu.com',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
		}
		

	def getXsrf(self):
		req=requests.get(self.login_url,headers=self.headers)
		cont=req.content
		soup=BeautifulSoup(cont,'html.parser')
		xsrf=soup.find('input',attrs={"name":"_xsrf"})
		print 'get xsrf sucess'
		return xsrf['value']

	def login(self,xsrf):
		headers=copy.copy(self.headers)
		headers['Referer']='https://www.zhihu.com/'
		headers['X-Xsrftoken']=xsrf
		datas={
		    '_xsrf':xsrf,
		    'email':'yunyu2010@yeah.net',
		    'password':'******',
		    'remember_me':'true'
		}
		req=requests.post(self.login_uri,data=datas,headers=headers)
		print 'login success'
		return req.cookies
		
	def getFollows(self,cookies):
		headers=copy.copy(self.headers)
		req=requests.get(self.follow_url,headers=headers,cookies=cookies)
		cont=req.content
		hxs=etree.HTML(cont)
		token=hxs.xpath('//input[@name="_xsrf"]/@value')[0]
		section=hxs.xpath('//span[@class="zm-profile-section-name"]/text()')[0]
		m=re.search('(\d+)',section)
		count=int(m.group(1))
		warp=hxs.xpath('//div[@class="zh-general-list clearfix"]')[0]
		params=warp.xpath('@data-init')[0]
		item=json.loads(params)
		nodename=item['nodename']
		hash_id=item['params']['hash_id']
		ls=warp.xpath('div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]')
		with codecs.open('follows.txt','a',encoding='utf-8') as fp:
			for i in ls:
				item=dict()
				data=list()
				a=i.xpath('a[@class="zm-item-link-avatar"]')[0]
				item['view_url']=a.xpath('@href')[0]
				item['name']=a.xpath('@title')[0]
				item['avatar']=a.xpath('img[@class="zm-item-img-avatar"]/@src')[0]
				descp=i.xpath('.//span[@class="bio"]/text()')
				item['descp']=descp[0] if descp else ''
				points=i.xpath('.//a[@class="zg-link-gray-normal"]/text()')
				for x in points:
					m=re.search('(\d+)',x)
					point=m.group(1) if m.groups() else 0
					data.append(point)
				item['data']=data
				line=json.dumps(item,ensure_ascii=True)
				fp.write('{0}\n'.format(line))
		return hash_id,token,count

	def getAjax(self,cookies,hash_id,token,offset):
		headers=copy.copy(self.headers)
		cookies=['{0}={1}'.format(item.name,item.value) for item in cookies]
		cookies.append('_xsrf={0}'.format(token))
		headers['Cookie']=';'.join(cookies)
		params={"offset":offset,"order_by":"created","hash_id":hash_id}
		datas={
			'method':'next',
			'params':json.dumps(params)
		}
		headers['Referer']='https://www.zhihu.com/people/excited-vczh/followees'
		headers['X-Requested-With']='XMLHttpRequest'
		headers['X-Xsrftoken']=token
		headers['Content-Type']="application/x-www-form-urlencoded; charset=UTF-8"
		req=requests.post('https://www.zhihu.com/node/ProfileFolloweesListV2',data=datas,headers=headers)
		cont=req.content
		items=json.loads(cont)
		with codecs.open('follows.txt','a',encoding='utf-8') as fp:
			for i in items['msg']:
				item=dict()
				data=list()
				hxs=etree.HTML(i)
				a=hxs.xpath('//a[@class="zm-item-link-avatar"]')[0]
				item['view_url']=a.xpath('@href')[0]
				item['name']=a.xpath('@title')[0]
				item['avatar']=a.xpath('//img[@class="zm-item-img-avatar"]/@src')[0]
				descp=hxs.xpath('//span[@class="bio"]/text()')
				item['descp']=descp[0] if descp else ''
				points=hxs.xpath('//a[@class="zg-link-gray-normal"]/text()')
				for x in points:
					m=re.search('(\d+)',x)
					point=m.group(1) if m.groups() else 0
					data.append(point)
				item['data']=data
				line=json.dumps(item,ensure_ascii=True)
				fp.write('{0}\n'.format(line))

	def run(self):
		xsrf=self.getXsrf()
		cookies=self.login(xsrf)
		hash_id,token,count=self.getFollows(cookies)
		pages=int(count//20+1)
		for i in range(1,pages):
			offset=i*20
			self.getAjax(cookies,hash_id,token,offset)
			print '{0}:{1} spider success'.format(i,offset)
			time.sleep(1)

	def WriteCookie(self,s):
		cookie=s.split(';')
		cookies=dict()
		map(lambda x:cookies.setdefault(x.split('=',1)[0],x.split('=',1)[1]),cookie)
		with codecs.open('e:/zhihu/cookie.log','a',encoding='utf-8') as fp:
			line=json.dumps(dict(cookies),ensure_ascii=True)
			fp.write(line)
		
if __name__ == '__main__':
	s='q_c1=079cd80429614ea1a9f211a6d0f24830|1477288506000|1477288506000; _xsrf=10a129a1972fbb0dbcafbda0fd1a62d7; l_cap_id="NDVkYTNiYTEyYTYxNDdiNDg0Zjk0NWQ2OGU5M2M4ZjU=|1477288506|397ece1c6e22a788059a1d41cdf38a0e5b977cd5"; cap_id="Y2FlYmExY2I3MjQzNDQwMzg3NmRiMjQ2ZTA1OTkzNTk=|1477288506|2269acb5fc34d46672cea630abd6a103fe6cc351"; d_c0="ABDA2BhkvQqPTuq5V3TadpBg1kPZPDp4U2Q=|1477288506"; _zap=92f05cdb-9abe-44a8-a924-5574146ace90; __utmt=1; login="MGIxNjBmYzYzN2ZlNGZjNzg1ZDJkYWQ3MzM3ZDk3YWU=|1477288518|0553ae6426d401468ccbf0fb33b5f36342055b89"; n_c=1; __utma=51854390.859254675.1477288835.1477288835.1477288835.1; __utmb=51854390.8.8.1477288853776; __utmc=51854390; __utmz=51854390.1477288835.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20150731=1^3=entry_date=20150731=1; a_t="2.0ABDKbo3deAgXAAAAhC81WAAQym6N3XgIABDA2BhkvQoXAAAAYQJVTUYvNVgA9EjcHj0g4dAcHEmF9EexFDM0QLDmqVZV9ZstiQ6S907Gle0ACksjtQ=="; z_c0=Mi4wQUJES2JvM2RlQWdBRU1EWUdHUzlDaGNBQUFCaEFsVk5SaTgxV0FEMFNOd2VQU0RoMEJ3Y1NZWDBSN0VVTXpSQXNB|1477288580|30f730ff444b82a7cbda423cc66f5ef41afb7bc7'
	follow=Follows()
	follow.WriteCookie(s)





