#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-08-09 16:39:25
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : 从美剧天堂下载美剧

import re
import urlparse
import urllib
import requests

class MeijuDownload(object):
	def __init__(self,url):
		self.url= url
		self.headers=dict()

	def setHeaders(self):
		headers=dict()
		parse=urlparse.urlparse(self.url)
		headers['Host']=parse.netloc
		headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
		return headers

	def getTasks(self,souce):
		self.headers=self.setHeaders()
		req=requests.get(self.url,headers=self.headers)
		cont=req.content.decode('gbk')
		rule=re.compile('"(ed2k://\|file\|[^"]*?1024X[^"]*?)".*?',re.S)
		vals=re.findall(rule,cont)
		tasks=set(vals)
		with open(souce,'ab') as fp:
			for val in tasks:
				value=urllib.quote(val.encode('utf-8'),safe="://|=")
				fp.write('{token}\n'.format(token=value))

		print 'successful,total {nums} tasks'.format(nums=len(tasks))

url=raw_input('please input the url(meijutiantang):')
source=raw_input('please input the save path:')
meiju=MeijuDownload(url)
meiju.getTasks(source)
