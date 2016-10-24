#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-09-28 14:36:58
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : requests及phantomjs模拟登陆知乎

import re
import copy
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def filterNumber(s):
	m=re.search('(\d+)',s)
	num=m.group(1) if m else 0
	return num

class Spider(object):
	"""模拟登陆知乎并获取关注的话题"""
	def __init__(self):
		self.login_url='https://www.zhihu.com/#signin'
		self.login_uri='https://www.zhihu.com/login/email'
		self.follow_url='https://www.zhihu.com/question/following'
		self.headers={
		    'Host':'www.zhihu.com',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
		}

	def getXsrf(self):
		"""使用requests请求https://www.zhihu.com/#signin并获取xsrf表单令牌值"""
		req=requests.get(self.login_url,headers=self.headers)
		cont=req.content
		#soup=BeautifulSoup(cont,'lxml')
		soup=BeautifulSoup(cont,'html.parser')
		xsrf=soup.find('input',attrs={"name":"_xsrf"})
		return xsrf['value']

	def getXsrf1(self):
		"""使用phantomjs组装header,请求https://www.zhihu.com/#signin并获取xsrf表单令牌值"""
		cap = webdriver.DesiredCapabilities.PHANTOMJS
		cap["phantomjs.page.settings.userAgent"] = self.headers['User-Agent']
		cap["phantomjs.page.settings.loadImages"] = False #禁止加载图片
		cap["phantomjs.page.settings.resourceTimeout"]=5000
		cap["phantomjs.page.customHeaders.Host"]=self.headers['Host']
		cap["phantomjs.page.customHeaders.Pragma"]=self.headers['Pragma']
		cap["phantomjs.page.customHeaders.Cache-Control"]=self.headers['Cache-Control']
		driver = webdriver.PhantomJS(desired_capabilities=cap,service_log_path='zhizhu.log')
		driver.get(self.login_url)
		xsrf=driver.find_element_by_name('_xsrf').get_attribute('value')
		driver.quit()
		return xsrf

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
		return req.cookies

	def getFollows1(self,cookies):
		"""使用phantomjs组装header及cookie,请求https://www.zhihu.com/question/following"""
		headers=copy.copy(self.headers)
		headers['Cookie']=';'.join(['{0}={1}'.format(item.name,item.value) for item in cookies])
		cap = webdriver.DesiredCapabilities.PHANTOMJS
		cap["phantomjs.page.settings.userAgent"] = headers['User-Agent']
		cap["phantomjs.page.settings.loadImages"] = False #禁止加载图片
		cap["phantomjs.page.settings.resourceTimeout"]=5000
		cap["phantomjs.page.customHeaders.Host"]=headers['Host']
		cap["phantomjs.page.customHeaders.Pragma"]=headers['Pragma']
		cap["phantomjs.page.customHeaders.Cache-Control"]=headers['Cache-Control']
		cap["phantomjs.page.customHeaders.Cookie"]=headers['Cookie']
		driver = webdriver.PhantomJS(desired_capabilities=cap,service_log_path='zhizhu.log')
		driver.get(self.follow_url)
		follows=driver.page_source
		driver.quit()
		return follows

	def getFollows(self,cookies):
		"""使用requests组装header及cookie请求https://www.zhihu.com/question/following"""
		req=requests.get(self.follow_url,headers=self.headers,cookies=cookies)
		follows=req.content
		return follows

	def getItems(self,follows):
		soup=BeautifulSoup(follows,'html.parser')
		topics=soup.find_all('div',attrs={'class':'zm-profile-section-item'})
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
		return items

	def run(self):
		#xsrf=self.getXsrf1()
		xsrf=self.getXsrf()
		cookies=self.login(xsrf)
		#follows=self.getFollows1(cookies)
		follows=self.getFollows(cookies)
		items=self.getItems(follows)
		return items

if __name__ == '__main__':
	spider=Spider()
	items=spider.run()
	for item in items:
		print 'topic:{title} link:https://www.zhihu.com{url} follow:{follow} scan:{scan} join:{answer}'.format(**item)

