#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-29 12:04:14
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import sys
import json
import time
import redis
import logging
import mysql.connector

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

def updateContById(data,view_url,song_id):
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			cursor1=db.cursor()
			if item['view_url']==view_url:
				created=int(time.time())
				try:
					sql1="update `content` set `title`=%s,`created`=%s,`view_url`=%s,`comment_num`=%s,`point`=%s,`content`=%s where id="+song_id
					cursor1.execute(sql1,[item['title'],created,item['view_url'],item['comment_nums'],item['point'],item['content']])
					cursor1.close()
				except mysql.connector.Error as e:
					msg=u'view_url:{url} 写入数据表{table}失败:{message}' .format(url=item['view_url'],table='content',message=e)
					logger.error(msg)
					cursor1.close()
				finally:
					cursor1.close()
			else:
				continue

def updateDynasty():
	dynasty=[u'先秦',u'两汉',u'魏晋',u'南北朝',u'隋代',u'唐代',u'五代',u'宋代',u'金朝',u'元代',u'明代',u'清代',u'近代',u'现代']
	cursor1=db.cursor()
	i=1
	while i<6:
		start=(i-1)*1000
		end=i*1000+1
		sql='select id,dynasty from author where id>%s and id<%s' % (start,end)
		cursor1.execute(sql)
		results=cursor1.fetchall()
		for result in results:
			if result[1] in dynasty:
				dynasty_id=dynasty.index(result[1])+1
				sql1='update author set dynasty_id=%s where id=%s'
				cursor1.execute(sql1,(dynasty_id,result[0]))
			else:
				continue
		print '%s-%s' % (start,end)
		i+=1

def updateContDynasty():
	cursor1=db.cursor()
	i=1
	while i<74:
		start=(i-1)*1000
		end=i*1000
		sql='select id,author_id from content where id>=%s and id<%s' % (start,end)
		cursor1.execute(sql)
		results=cursor1.fetchall()
		for result in results:
			if result[1]!=0:
				sql1='select dynasty_id,name from author where id=%s' % result[1]
				cursor1.execute(sql1)
				author=cursor1.fetchone()
				author_id=result[1]
				filter_dy=[u'佚名',u'未知作者']
				if author[1] in filter_dy:
					author_id=0
				dynasty_id=author[0]
				try:
					sql2='update `content` set `author_id`=%s,`dynasty_id`=%s where id=%s'
					cursor1.execute(sql2,(author_id,dynasty_id,result[0]))
				except mysql.connector.Error as e:
					msg=u'id:%s update error:%s' % (result[0],str(e))
					logger.error(msg)
					cursor1.close()
			else:
				print result[0]
				continue
		print '%s-%s' % (start,end)
		i+=1

def updateContRelationUrls(data):
	try:
		pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
		redis_conn = redis.Redis(connection_pool=pool)
	except redis.RedisError as e:
		msg='redis connect error %s' % str(e)
		logger.error(msg)
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			if item['relation_urls'] and redis_conn.hexists('article',item['view_url']):
				cursor1=db.cursor()
				relation_urls=','.join(item['relation_urls'])
				article_id=redis_conn.hget('article',item['view_url'])
				sql='update `content` set `relation_urls`=%s where id=%s'
				cursor1.execute(sql,(relation_urls,article_id))
				print '%s-%s update sucess' % (item['view_url'],article_id)

def updateContRelationById(data,view_url,ids):
	try:
		pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
		redis_conn = redis.Redis(connection_pool=pool)
	except redis.RedisError as e:
		msg='redis connect error %s' % str(e)
		logger.error(msg)
	with open(data,'r') as fp:
		for line  in fp.readlines():
			item=json.loads(line)
			if item['rel_url']==view_url:
				cursor1=db.cursor()
				created=int(time.time())
				article_id=redis_conn.hget('article',item['view_url'])
				sql='update `content_relation` set `cont_id`=%s,`title`=%s,`descrption`=%s,`created`=%s,`view_url`=%s,`editor`=%s where id=%s'
				cursor1.execute(sql,(article_id,item['rel_title'],item['rel_content'],created,item['rel_url'],item['editor'],ids))
			else:
				continue

def updateAuthor(data,author_url,author_id):
	with open(data) as fp:
		flag=True
		for line in fp:
			item=json.loads(line)
			cursor1=conn.cursor()
			if item['author_url']==author_url:
				if flag:
					relation_urls=','.join(item['relation_urls']) if item['relation_urls'] else ''
					sql='update author set author_url=%s,faceimg=%s,descp=%s,relation_urls=%s where id=%s'
					try:
						cursor1.execute(sql,[item['author_url'],item['faceimg'],item['author_desc'],relation_urls,author_id])
					except mysql.connector.Error as e:
						msg='url:{url} message:{msg}'.format(url=author_url,msg=str(e))
						logger.error(msg)
					flag=False
				if item['relation_urls'] and 'view_url' in item:
					created=int(time.time())
					sql1='insert into author_relation (`author_id`,`title`,`description`,`created`,`editor`,`view_url`) values (%s,%s,%s,%s,%s,%s)'
					try:
						cursor1.execute(sql1,[author_id,item['title'],item['content'],created,item['editor'],item['view_url']])
					except  mysql.connector.Error as e:
						msg= 'url:{url} message:{msg}'.format(url=item['view_url'],msg=str(e))
						logger.error(msg)

if __name__ == '__main__':
	#updateDynasty()
	#updateContDynasty()
	data=sys.argv[1]
	#updateContRelationUrls(data)
	view_url=sys.argv[2]
	ids=sys.argv[3]
	#updateContById(data,view_url,ids)
	updateContRelationById(data,view_url,ids)