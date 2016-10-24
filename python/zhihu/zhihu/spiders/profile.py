#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-19 10:56:31
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import os
import json
import codecs
import scrapy
import urlparse
from urllib import urlencode
from scrapy.http import Request
from zhihu.functions import stripHtml
from scrapy.selector import Selector
from zhihu.items import PeopleItem,ActiveItem
from zhihu.settings import LOG_FILE,DATAS,DEFAULT_REQUEST_HEADERS

class Profile(scrapy.Spider):
	"""docstring for Profile"""
	name='profile'
	allowed_domains=["www.zhihu.com"]
	start_urls=[]

	def __init__(self,*args,**kwargs):
		super(Profile,self).__init__(*args, **kwargs)
		self.headers=DEFAULT_REQUEST_HEADERS
		source_root=os.path.dirname(LOG_FILE)
		self.profile_souce='{0}/{1}'.format(source_root,DATAS['profile'])
		self.actives_source='{0}/{1}'.format(source_root,DATAS['actives'])
		self.followees_source='{0}/{1}'.format(source_root,DATAS['followees'])
		self.addCookie(source_root)

	def addCookie(self,source_root):
		cookie_file='{0}/{1}'.format(source_root,DATAS['cookies'])
		with open(cookie_file,'r') as fp:
			cont=fp.read()
		self.cookies=json.loads(cont)

	def getPeoples(self):
		people=list()
		with codecs.open(self.followees_source,'r',encoding='utf-8') as fp:
			for line in fp.readlines():
				item=json.loads(line)
				url='https://{0}{1}'.format(self.allowed_domains[0],item['view_url'])
				people.append(url)
		return people

	def start_requests(self):
		self.start_urls=self.getPeoples()
		for url in self.start_urls:
			yield Request(url,headers=self.headers,cookies=self.cookies,callback=self.parse_item,errback=self.catchError)

	def catchError(self,response):
		pass

	def parse_item(self,response):
		url_page=response.url
		parse_urls=urlparse.urlparse(url_page)
		print 'start spider {0} lastes 20'.format(parse_urls.path)
		hxs=Selector(response)
		profile=PeopleItem()
		profile_warp=hxs.xpath('//div[@class="zm-profile-header ProfileCard"]')
		token=hxs.xpath('//input[@name="_xsrf"]/@value').extract()[0]
		location=profile_warp.xpath('//span[@class="location item"]/@title').extract()
		business=profile_warp.xpath('//span[@class="business item"]/@title').extract()
		gender_i=profile_warp.xpath('//span[@class="item gender"]/i/@class').extract()
		gender=gender_i[0].split()[1].split('-')[-1] if gender_i else ''
		employment=profile_warp.xpath('//span[@class="employment item"]/@title').extract()
		position=profile_warp.xpath('//span[@class="position item"]/@title').extract()
		education=profile_warp.xpath('//span[@class="education item"]/@title').extract()
		education_extra=profile_warp.xpath('//span[@class="education-extra item"]/@title').extract()
		content=profile_warp.xpath('//span[@class="fold-item"]').css('.content').extract()
		profile['user_page']=url_page
		profile['location']=location[0].strip() if location else ''
		profile['business']=business[0].strip() if business else ''
		profile['gender']=gender
		profile['employment']=employment[0].strip() if employment else ''
		profile['position']=position[0].strip() if position else ''
		profile['education']=education[0].strip() if education else ''
		profile['education_extra']=education_extra[0] if education_extra else ''
		profile['content']=stripHtml(content[0]) if content else ''
		answer_wap=hxs.xpath('//div[@id="zh-profile-answers-inner-list"]').css('.zm-profile-section-item')
		answers=list()
		for i in answer_wap:
			answer=dict()
			num=i.css('.zm-profile-vote-num::text').extract()
			a=i.css('.question_link')
			title=a.xpath('./text()').extract()[0]
			link=a.xpath('./@href').extract()[0]
			descp=i.css('.zm-profile-item-text::text').extract()
			answer['num']=num[0] if num else ''
			answer['title']=title
			answer['link']=link
			answer['descp']=descp[0]
			answers.append(answer)

		profile['answers']=answers
		with codecs.open(self.profile_souce,'a',encoding='utf-8') as fp:
			line=json.dumps(dict(profile),ensure_ascii=True)
			fp.write('{0}\n'.format(line))
		
		active_warp=hxs.xpath('//div[@id="zh-profile-activity-page-list"]')
		ls=active_warp.xpath('div[@class="zm-profile-section-item zm-item clearfix"]')
		actives=list()
		for i in ls:
			data=dict()
			created=i.xpath('./@data-time').extract()[0]
			active_main=i.css('.zm-profile-section-activity-main')
			a=active_main.css('.question_link')
			b=active_main.css('.post-link')
			posts=None
			if a:
				posts=a
			elif b:
				posts=b
			if posts:
				link=posts.xpath('./@href').extract()
				title=posts.xpath('./text()').extract()
				data['title']=title[0].replace('\n','')
				data['link']=link[0]
			temp=active_main.extract()
			active=stripHtml(temp[0]) if temp else ''
			item_anser=i.css('.zm-item-answer')
			item_post=i.css('.zm-item-post')
			post_main=None
			if item_anser:
				post_main=item_anser
			elif item_post:
				post_main=item_post
			if post_main:
				author_link=post_main.css('.author-link::attr(href)').extract()
				author=post_main.css('.author-link::text').extract()
				summary_temp=post_main.css('.zh-summary').extract()
				summary_temp=''.join(summary_temp)
				summary=stripHtml(summary_temp) if summary_temp else ''
				data['summary']=summary.strip(u'显示全部')
				data['author']=author[0] if author else u'匿名用户'
				data['author_link']=author_link[0] if author_link else ''
			data['created']=created
			data['active']=active
			actives.append(data)
		contents=ActiveItem()
		contents['url_page']=url_page
		contents['starts']='0'
		contents['actives']=actives
		with codecs.open(self.actives_source,'a',encoding='utf-8') as fp:
			line=json.dumps(dict(contents),ensure_ascii=True)
			fp.write('{0}\n'.format(line))

		self.headers['Referer']=url_page
		self.headers['X-Requested-With']='XMLHttpRequest'
		self.headers['X-Xsrftoken']=token
		self.headers['Content-Type']='application/x-www-form-urlencoded; charset=UTF-8'
		starts=actives[-1]['created']
		datas={'start':starts}
		print 'start ajax spider {0},offset {1}'.format(parse_urls.path,starts)
		url='{0}/activities'.format(url_page)
		yield Request(url,method="POST",headers=self.headers,body=urlencode(datas),callback=self.parse_active_ajax,errback=self.catchError,meta={'url_page':url_page,'starts':starts})

	def parse_active_ajax(self,response):
		url=response.url
		parse_urls=urlparse.urlparse(url)
		url_page=response.meta['url_page']
		start_meta=response.meta['starts']
		cont=json.loads(response.body_as_unicode())
		if cont['msg'][1]:
			print 'ajax spider {0} success,offset {1}'.format(parse_urls.path,start_meta)
			hxs=Selector(text=cont['msg'][1])
			ls=hxs.xpath('//div[@class="zm-profile-section-item zm-item clearfix"]')
			actives=list()
			with codecs.open(self.actives_source,'a',encoding='utf-8') as fp:
				item=ActiveItem()
				for i in ls:
					data=dict()
					created=i.xpath('./@data-time').extract()[0]
					active_main=i.css('.zm-profile-section-activity-main')
					a=active_main.css('.question_link')
					b=active_main.css('.post-link')
					posts=None
					if a:
						posts=a
					elif b:
						posts=b
					if posts:
						link=posts.xpath('./@href').extract()
						title=posts.xpath('./text()').extract()
						data['title']=title[0].replace('\n','')
						data['link']=link[0]
					temp=active_main.extract()
					active=stripHtml(temp[0]) if temp else ''
					item_anser=i.css('.zm-item-answer')
					item_post=i.css('.zm-item-post')
					post_main=None
					if item_anser:
						post_main=item_anser
					elif item_post:
						post_main=item_post
					if post_main:
						author_link=post_main.css('.author-link::attr(href)').extract()
						author=post_main.css('.author-link::text').extract()
						summary_temp=post_main.css('.zh-summary').extract()
						summary_temp=''.join(summary_temp)
						summary=stripHtml(summary_temp) if summary_temp else ''
						data['summary']=summary.strip(u'显示全部')
						data['author']=author[0] if author else u'匿名用户'
						data['author_link']=author_link[0] if author_link else ''
					data['created']=created
					data['active']=active
					actives.append(data)
				item['url_page']=url_page
				item['actives']=actives
				item['starts']=start_meta
				line=json.dumps(dict(item),ensure_ascii=True)
				fp.write('{0}\n'.format(line))
			start_next=actives[-1]['created']
			data={'start':start_next}
			self.headers['Referer']=url_page
			print 'start ajax spider {0},offset {1}'.format(parse_urls.path,start_next)
			yield Request(url,headers=self.headers,method="POST",body=urlencode(data),callback=self.parse_active_ajax,errback=self.catchError,meta={'url_page':url_page,'starts':start_next})
		else:
			print 'ajax spider {0} faild,offset {1}'.format(parse_urls.path,start_meta)
		