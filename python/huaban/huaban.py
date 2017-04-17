#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-02 15:25:40
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description
from __future__ import division
import re
import os
import time
import json
import math
import codecs
import logging
import urlparse
import requests
import mysql.connector
from selenium import webdriver

class HuabanSpider(object):
	"""采集花瓣美女摄影"""
	def __init__(self,url,json_path):
		self.headers={'Host':'huaban.com','Pragma':'no-cache','Cache-Control':'no-cache'}
		self.source_url=url
		self.json_path=json_path
		self.page_count=0
		self.pagesize=20
		self.last_pin=0
		self.getLogger('error.log')

	def getLogger(self,error_path):
		logger=logging.getLogger('huaban')
		formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
		logger.setLevel(logging.ERROR)
		root='{0}/{1}'.format(os.path.dirname(os.path.realpath(__file__),),error_path)
		handler=logging.FileHandler(root,mode='a',encoding='utf-8')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		self.logger=logger

	def getFirst(self):
		"""
		req=requests.get(url,headers=headers)
		cont=req.content
		rule=re.compile('app\.page\["board"\] = {(.*?)};',re.S)
		m=re.search(rule,cont)
		temp='{{{0}}}'.format(m.group(1))
		warp=json.loads(temp)
		"""
		cap = webdriver.DesiredCapabilities.PHANTOMJS
		cap["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'
		cap["phantomjs.page.settings.loadImages"] = False #禁止加载图片
		cap["phantomjs.page.settings.resourceTimeout"]=5000
		cap["phantomjs.page.customHeaders.Host"]=self.headers['Host']
		cap["phantomjs.page.customHeaders.Pragma"]=self.headers['Pragma']
		cap["phantomjs.page.customHeaders.Cache-Control"]=self.headers['Cache-Control']
		driver = webdriver.PhantomJS(desired_capabilities=cap)
		driver.get(self.source_url)
		warp=driver.execute_script('return app.page["board"]')
		if warp:
			pins=warp['pins']
			pins_count=warp['pin_count']
			print pins_count
			self.page_count=int(math.ceil(pins_count/self.pagesize))
			self.last_pin=pins[-1]['pin_id']
			self.outJson(pins)
		else:
			print 'error'
			exit()

	def getNext(self,i):
		self.headers['Accept']='application/json'
		self.headers['X-Requested-With']='XMLHttpRequest'
		self.headers['X-Request']='JSON'
		url='{0}?max={1}&limit={2}&wfl=1'.format(self.source_url,self.last_pin,self.pagesize)
		print '{0}:{1}'.format(i,url)
		req=requests.get(url,headers=self.headers)
		cont=req.content
		warp=json.loads(cont)
		pins=warp['board']['pins']
		if pins:
			self.last_pin=pins[-1]['pin_id']
			self.outJson(pins)
		else:
			print 'game over'
			exit()

	def outJson(self,pins):
		with codecs.open(self.json_path,'a',encoding='utf-8') as fp:
			for i in pins:
				item=dict()
				item['user_id']=i['user_id']
				item['file_id']=i['file_id']
				item['link']=i['link']
				item['file']=i['file']
				item['comment_count']=i['comment_count']
				item['created']=i['created_at']
				item['like']=i['like_count']
				item['pin_id']=i['pin_id']
				item['meta']=i['text_meta']
				item['raw']=i['raw_text']
				item['repin_count']=i['repin_count']
				item['source']=i['source']
				item['via']=i['via']
				item['via_user_id']=i['via_user_id']
				item['original']=i['original']
				item['img']='{0}/{1}'.format('http://img.hb.aicdn.com',i['file']['key'])
				line=json.dumps(item,ensure_ascii=True)
				fp.write('{0}\n'.format(line))

	def run(self):
		self.getFirst()
		i=1
		while i<self.page_count:
			self.getNext(i)
			i+=1
			time.sleep(1)

	def importMysql(self):
		if not os.path.exists(self.json_path):
			msg=u'{1}数据文件不存在'.format(self.json_path)
			self.logger.error(msg)
			exit()
		try:
			db = mysql.connector.connect(host='127.0.0.1',user='root', password='123456', database='huaban',charset='utf8')
		except mysql.connector.Error as e:
			msg=u'数据库连接失败:%s' % str(e)
			self.logger.error(msg)
			exit()
		with codecs.open(self.json_path,'r',encoding='utf-8') as fp:
			for line in fp.readlines():
				item=json.loads(line)
				cursor=db.cursor()
				try:
					sql="insert into `photogirls` (`user_id`,`like`,`image`,`created`,`via`,`pin_id`,`repin_count`,`original`,`raw`,`comment_count`,`meta`,`link`,`file_id`,`via_user_id`,`source`,`img_type`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
					meta=''
					img_type=''
					if item['meta']:
						meta=json.dumps(item,ensure_ascii=True)
					if item['file']['type']:
						types=item['file']['type'].split('/',1)
						img_type=types[1] if len(types)>1 else types[0]
						img_type=img_type.lower()
					params=(item['user_id'],item['like'],item['img'],item['created'],item['via'],item['pin_id'],item['repin_count'],item['original'],item['raw'],item['comment_count'],meta,item['link'],item['file_id'],item['via_user_id'],item['source'],img_type)
					cursor.execute(sql,params)
					"""
					#When you use a transactional storage engine such as InnoDB (the default in MySQL 5.5 and higher), you must commit the data after a sequence of INSERT, DELETE, and UPDATE statements.
					db.commit()
					"""
				except mysql.connector.Error as e:
					msg=u'via:{via} 写入数据表{table}失败:{reasion}'.format(via=item['via'],table='photogirls',reasion=e)
					self.logger.error(msg)
					cursor.close()

	def saveimg(self,distpath,img_url,extension):
		headers={
		'Host':'img.hb.aicdn.com',
		'Referer':self.source_url,
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		}
		if not os.path.exists(distpath):
			os.mkdir(distpath)
		print 'begin:{0}'.format(img_url)
		query=urlparse.urlparse(img_url)
		save_name=query.path[1:]
		try:
			req=requests.get(img_url,headers=headers,timeout=5)
			distname='{0}/{1}.{2}'.format(distpath,save_name,extension)
			fs=open(distname,'wb')
			fs.write(req.content)
			fs.close()
			print 'end:{0}'.format(img_url)
		except requests.exceptions.Timeout:
			msg='download {0} timeout'.format(img_url)
			print msg
			self.logger.error(msg)

	def downImage(self,dirnames):
		root=os.path.dirname(os.path.realpath(__file__))
		image_path='{0}/{1}'.format(root,dirnames)
		if not os.path.exists(image_path):
			print 'mkdir {0} folder'.format(dirnames)
			os.mkdir(image_path)
		with codecs.open(self.json_path,'r',encoding='utf-8') as fp:
			for line in fp.readlines():
				item=json.loads(line)
				print 'down:{0}'.format(item['via'])
				types=item['file']['type'].split('/',1)
				img_type=types[1] if len(types)>1 else types[0]
				img_type=img_type.lower()
				distpath='{0}/{1}'.format(image_path,item['pin_id'])
				thumb_url='{0}{1}'.format(item['img'],'_fw236')
				self.saveimg(distpath,item['img'],img_type)
				self.saveimg(distpath,thumb_url,img_type)
				time.sleep(1)

if __name__ == '__main__':
	huaban=HuabanSpider('http://huaban.com/boards/28195582','d:/python/zhihu/huanban.json')
	huaban.downImage('images')