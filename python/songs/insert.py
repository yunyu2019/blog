#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-07 18:33:36
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import sys
import json
import time
import redis
import logging
import mysql.connector
from pypinyin import lazy_pinyin

logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
handler=logging.FileHandler('/home/www/songs/mysql_error.log',mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
	db = mysql.connector.connect(host='127.0.0.1',user='root', password='123456', database='songs',charset='utf8mb4')
except mysql.connector.Error as e:
	msg=u'数据库连接失败:%s' % str(e)
	logger.error(msg)

try:
	pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
	redis_conn = redis.Redis(connection_pool=pool)
except redis.RedisError as e:
	msg='redis connect error %s' % str(e)
	logger.error(msg)

def InAuthor(data):
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			relation_urls=','.join(item['relation_urls'])
			cursor1=db.cursor()
			try:
				author_id=0
				if redis_conn.hexists('author',item['author_id']):
					author_id=redis_conn.hget('author',item['author_id'])
				else:
					sql="insert into `author` (`name`,`dynasty`,`author_url`,`faceimg`,`descp`,`pinyin`,`relation_urls`) values(%s,%s,%s,%s,%s,%s,%s)"
					cursor1.execute(sql,[item['author'],item['dynasty'],item['author_url'],item['faceimg'],item['author_desc'],item['pinyin'],relation_urls])
					author_id=str(cursor1.lastrowid)
					redis_conn.hsetnx('author',item['author_id'],author_id)
				if item['relation_urls']:
					sql="insert into `author_relation` (`author_id`,`title`,`description`,`created`,`editor`,`view_url`) values(%s,%s,%s,%s,%s,%s)"
					created=int(time.time())
					cursor1.execute(sql,[author_id,item['title'],item['content'],created,item['editor'],item['view_url']])
			except mysql.connector.Error as e:
				msg=u'author_url:%s 写入数据失败:%s' % (item['author_url'],e)
				logger.error(msg)
				cursor1.close()

def InDynasty():
	dynasty=[u'先秦',u'两汉',u'魏晋',u'南北朝',u'隋代',u'唐代',u'五代',u'宋代',u'金朝',u'元代',u'明代',u'清代']
	cursor1=db.cursor()
	for x in dynasty:
		created=int(time.time())
		sql="insert into `dynasty` (`name`,`created`) values(%s,%s)"
		try:
			cursor1.execute(sql,(x,created))
		except mysql.connector.Error as e:
			msg='insert into dynasty error:%s' % (str(e))
			logger.error(msg)
			cursor1.close()
	print 'sucess'

def InsertSongs(data):
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			cursor1=db.cursor()
			try:
				author_id=0
				keys=lazy_pinyin(item['author']+'_'+item['dynasty'])
				key=''.join(keys)
				kwd=''
				if redis_conn.hexists('author',item['author_id']):
					kwd=item['author_id']
				elif redis_conn.hexists('author',key):
					kwd=key
				if kwd!='':
					author_id=redis_conn.hget('author',kwd)
				else:
					sql="insert into `author` (`name`,`dynasty`,`pinyin`) values(%s,%s,%s)"
					cursor1.execute(sql,[item['author'],item['dynasty'],item['pinyin']])
					author_id=str(cursor1.lastrowid)
					redis_conn.hsetnx('author',key,author_id)
				created=int(time.time())
				sql1="insert into `content` (`author_id`,`title`,`created`,`view_url`,`comment_num`,`point`,`content`) values(%s,%s,%s,%s,%s,%s,%s)"
				cursor1.execute(sql1,[author_id,item['title'],created,item['view_url'],item['comment_nums'],item['point'],item['content']])
				cursor1.close()
			except mysql.connector.Error as e:
				msg=u'view_url:%s 写入数据失败:%s' % (item['view_url'],e)
				logger.error(msg)
				cursor1.close()
			finally:
				cursor1.close()

if __name__ == '__main__':
	"""
	data=sys.argv[1]
	InAuthor(data)
	"""
	InDynasty()
	"""
	data=sys.argv[1]
	InsertSongs(data)
	"""
	



