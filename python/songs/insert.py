#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-07 18:33:36
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import os
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
root='{app}/mysql_error.log'.format(app=os.path.dirname(os.path.realpath(__file__)))
handler=logging.FileHandler(root,mode='a',encoding='utf-8')
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

def InsertAuthor(data):
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			relation_urls=','.join(item['relation_urls'])
			cursor1=db.cursor()
			author_id=0
			if redis_conn.hexists('author',item['author_id']):
				author_id=redis_conn.hget('author',item['author_id'])
			else:
				try:
					sql="insert into `author` (`name`,`dynasty`,`author_url`,`faceimg`,`descp`,`pinyin`,`relation_urls`) values(%s,%s,%s,%s,%s,%s,%s)"
					cursor1.execute(sql,[item['author'],item['dynasty'],item['author_url'],item['faceimg'],item['author_desc'],item['pinyin'],relation_urls])
					author_id=str(cursor1.lastrowid)
					redis_conn.hsetnx('author',item['author_id'],author_id)
				except mysql.connector.Error as e:
					msg=u'author_url:{url} 写入数据表{table}失败:{message}'.format(url=item['author_url'],table='author',message=e)
					logger.error(msg)
					cursor1.close()
			if item['relation_urls']:
				try:
					sql="insert into `author_relation` (`author_id`,`title`,`description`,`created`,`editor`,`view_url`) values(%s,%s,%s,%s,%s,%s)"
					created=int(time.time())
					cursor1.execute(sql,[author_id,item['title'],item['content'],created,item['editor'],item['view_url']])
				except mysql.connector.Error as e:
					msg=u'view_url:{url} 写入数据表{table}失败:{reasion}'.format(url=item['view_url'],table='author_relation',reasion=e)
					logger.error(msg)
					cursor1.close()

def InsertDynasty():
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
			if redis_conn.hexists('article',item['view_url']):
				if item['relation_urls']:
					article_id=redis_conn.hget('article',item['view_url'])
					created=int(time.time())
					try:
						sql="insert into `content_relation` (`cont_id`,`title`,`created`,`descrption`,`view_url`,`editor`) values(%s,%s,%s,%s,%s,%s)"
						cursor1.execute(sql,[article_id,item['rel_title'],created,item['rel_content'],item['rel_url'],item['editor']])
					except mysql.connector.Error as e:
						msg=u'view_url:{url} 写入数据表{table}失败:{message}'.format(url=item['rel_url'],table='content_relation',message=e)
						logger.error(msg)
						cursor1.close()
					finally:
						cursor1.close()
			else:
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
					try:
						sql="insert into `author` (`name`,`dynasty`,`pinyin`) values(%s,%s,%s)"
						cursor1.execute(sql,[item['author'],item['dynasty'],item['pinyin']])
						author_id=str(cursor1.lastrowid)
						redis_conn.hsetnx('author',key,author_id)
					except mysql.connector.Error as e:
						msg=u'view_url:{url} 写入数据表{table}失败:{message}'.format(url=item['view_url'],table='author',message=e)
						logger.error(msg)
						cursor1.close()	
				created=int(time.time())
				article_id=0
				sql1="insert into `content` (`author_id`,`title`,`created`,`view_url`,`comment_num`,`point`,`content`,`relation_urls`) values(%s,%s,%s,%s,%s,%s,%s,%s)"
				relation_urls=','.join(item['relation_urls']) if item['relation_urls'] else ''
				try:
					cursor1.execute(sql1,[author_id,item['title'],created,item['view_url'],item['comment_nums'],item['point'],item['content'],relation_urls])
					article_id=str(cursor1.lastrowid)
					redis_conn.hsetnx('article',item['view_url'],article_id)
				except mysql.connector.Error as e:
					msg=u'view_url:{url} 写入数据表{table}失败:{message}'.format(url=item['view_url'],table='content',message=e)
					logger.error(msg)
					cursor1.close()
				if item['relation_urls']:
					created=int(time.time())
					sql2="insert into `content_relation` (`cont_id`,`title`,`created`,`descrption`,`view_url`,`editor`) values(%s,%s,%s,%s,%s,%s)"
					try:
						cursor1.execute(sql2,[article_id,item['rel_title'],created,item['rel_content'],item['rel_url'],item['editor']])
					except mysql.connector.Error as e:
						msg=u'view_url:{url} 写入数据表{table}失败:{message}'.format(url=item['rel_url'],table='content_relation',message=e)
						logger.error(msg)
						cursor1.close()	
				else:
					continue

def InsertSongRedis():
	cursor1=db.cursor()
	i=1
	while i<74:
		start=(i-1)*1000
		end=i*1000
		sql='select id,view_url from content where id>=%s and id<%s' % (start,end)
		cursor1.execute(sql)
		results=cursor1.fetchall()
		for result in results:
			redis_conn.hsetnx('article',result[1],result[0])
		print '%s-%s' % (start,end)
		i+=1

if __name__ == '__main__':
	#InsertSongRedis()
	data=sys.argv[1]
	#insertAuthor(data)
	InsertSongs(data)
