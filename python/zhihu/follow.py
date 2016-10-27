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
		if isinstance(cookies,str):
			headers['Cookie']=cookies
		else:
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
		if items['msg']:
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
	follow=Follows()
	follow.run()





