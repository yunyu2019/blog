#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-13 14:10:48
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import os
import time
import json
import codecs
import scrapy
import requests
from urllib import urlencode
from scrapy.selector import Selector
from zhihu.items import FollowItem
from scrapy.http import Request,FormRequest
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from zhihu.settings import ZHIHU,LOG_FILE,DATAS,DEFAULT_REQUEST_HEADERS

class Follow(CrawlSpider):
	"""docstring for Follow"""
	name='follow'
	allowed_domains=["www.zhihu.com"]
	start_urls=["https://www.zhihu.com/people/excited-vczh/followees"]
	rules = (
	    Rule(LinkExtractor(allow=("/people/excited-vczh/followees",)),  callback='parse_followee',follow=False),
	)

	def __init__(self,*args,**kwargs):
		super(Follow, self).__init__(*args, **kwargs)
		source_root=os.path.dirname(LOG_FILE)
		self.headers=DEFAULT_REQUEST_HEADERS
		self.data_file='{0}/{1}'.format(source_root,DATAS['followees'])
		self.cookie_file='{0}/{1}'.format(source_root,DATAS['cookies'])
		self.captcha_file='{0}/{1}'.format(source_root,'captcha.gif')
		self.captcha=False

	def start_requests(self):
		return [Request('https://www.zhihu.com/#signin',meta = {'cookiejar' : 1}, callback = self.post_login)]

	def post_login(self,response):
		print 'Preparing login'
		hxs=Selector(response)
		xsrf=hxs.xpath('//input[@name="_xsrf"]/@value')[0].extract()
		formdata={'_xsrf': xsrf,'email':ZHIHU['email'],'password': ZHIHU['password'],'remember_me':'true'}
		if self.captcha:
			signform=hxs.xpath('//div[@class="view view-signin"]')
			captcha_type=signform.css('.captcha-module::attr(data-type)').extract()[0]
			self.getCaptcha(captcha_type)
			
			hint=''
			if captcha_type=='cn':
				formdata['captcha_type']=captcha_type
				hint=",the value like {\"img_size\":[200,44],\"input_points\":[[17.375,24],[161.375,20]]}"
			msg='please input the captch{0}\n'.format(hint)
			captcha=raw_input(msg)
			formdata['captcha']=json.dumps(captcha)
		return [FormRequest(ZHIHU['login_url'],formdata = formdata,method='POST',callback = self.after_login,dont_filter=True)]

	def getCaptcha(self,type):
		r=int(1000*time.time())
		captcha_url='{0}/captcha.gif?r={1}&type=login&lang={2}'.format(self.allowed_domains[0],r,type)
		headers=self.headers
		headers['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17'
		req=requests.get(captcha_url,headers=headers)
		captcha=req.content
		with open(self.captcha_file,'wb') as fp:
			fp.write(captcha)

	def after_login(self,response):
		res=json.loads(response.body_as_unicode())
		if 'errorcode' in res:
			errcode=res['errorcode']
			if errcode==1991829:
				print 'captcha required'
				self.captcha=True
				self.start_requests()
			else:
				print res['msg']
		else:
			print res['msg']
			for url in self.start_urls :
				yield self.make_requests_from_url(url)

	def catchError(self,response):
		pass

	def parse_followee(self,response):
		print 'spider follows begin'
		user_url=response.url
		cookie = response.request.headers.getlist('Cookie')[0].split(';')
		cookies=dict()
		map(lambda x:cookies.setdefault(x.split('=',1)[0],x.split('=',1)[1]),cookie)
		with codecs.open(self.cookie_file,'a',encoding='utf-8') as fp:
			line=json.dumps(dict(cookies),ensure_ascii=True)
			fp.write(line)
		hxs=Selector(response)
		section=hxs.xpath('//span[@class="zm-profile-section-name"]/text()').re('(\d+)')
		nums=int(section[0])
		token=hxs.xpath('//input[@name="_xsrf"]/@value').extract()[0]
		warp=hxs.xpath('//div[@class="zh-general-list clearfix"]')
		params_init=warp.xpath('@data-init').extract()[0]
		params=json.loads(params_init)
		hash_id=params['params']['hash_id']
		nodename=params['nodename']
		ls=warp.xpath('div[@class="zm-profile-card zm-profile-section-item zg-clear no-hovercard"]')
		with codecs.open(self.data_file,'a',encoding="utf-8") as fp:
			for v in ls:
				item=FollowItem()
				a=v.xpath('a[@class="zm-item-link-avatar"]')
				name=a.xpath('@title').extract()[0]
				view_url=a.xpath('@href').extract()[0]
				avatar=a.xpath('img[@class="zm-item-img-avatar"]/@src').extract()
				descp=v.css('.bio::text').extract()
				descp=descp[0] if descp else ''
				avatar=avatar[0] if avatar else ''
				points=v.css('.zg-link-gray-normal::text').re('(\d+)')
				item['name']=name
				item['avatar']=avatar
				item['view_url']=view_url
				item['descp']=descp
				item['data']=points
				line=json.dumps(dict(item),ensure_ascii=True)
				fp.write('{0}\n'.format(line))
		
		pages=int(nums//20+1)
		url='https://www.zhihu.com/node/{0}'.format(nodename)
		self.headers['Referer']=user_url
		self.headers['X-Requested-With']='XMLHttpRequest'
		self.headers['X-Xsrftoken']=token
		self.headers['User-Agent']='Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
		self.headers['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
		for i in range(1,pages):
			offset=i*20
			params={"offset":offset,"order_by":"created","hash_id":hash_id}
			print params
			datas={
				'method':'next',
				'params':json.dumps(params)
			}
			yield Request(url,method="POST",headers=self.headers,body=urlencode(datas),callback=self.parse_followees)


	def parse_followees(self,response):
		print 'ajax-followees'
		cont=json.loads(response.body_as_unicode())
		with codecs.open(self.data_file,'a',encoding='utf-8') as fp:
			for i in cont['msg']:
				item=FollowItem()
				hxs=Selector(text=i)
				a=hxs.xpath('//a[@class="zm-item-link-avatar"]')
				view_url=a.xpath('./@href').extract()[0]
				name=a.xpath('./@title').extract()[0]
				avatar=a.xpath('./img[@class="zm-item-img-avatar"]/@src').extract()[0]
				descp=hxs.xpath('//span[@class="bio"]/text()').extract()
				points=hxs.xpath('//a[@class="zg-link-gray-normal"]/text()').re('(\d+)')
				item['view_url']=view_url
				item['name']=name
				item['avatar']=avatar
				item['descp']=descp[0] if descp else ''
				item['data']=points
				line=json.dumps(dict(item),ensure_ascii=True)
				fp.write('{0}\n'.format(line))

		


			
			
		





