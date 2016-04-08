# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import time
import redis
import codecs
import logging
import mysql.connector
from songs import settings
from pypinyin import lazy_pinyin

logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
handler=logging.FileHandler('/home/www/songs/error.log',mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class SongsPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class AuthorPipeline(object):
    def __init__(self):
        mysql_db=settings.MYSQL_DB
        try:
            self.db = mysql.connector.connect(host=mysql_db['host'],user=mysql_db['user'], password=mysql_db['password'], database=mysql_db['database'],charset=mysql_db['charset'])
        except mysql.connector.Error as e:
            msg=u'数据库连接失败:%s' % str(e)
            logger.error(msg)
        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            self.redis_conn = redis.Redis(connection_pool=pool)
        except redis.RedisError as e:
            msg='redis connect error %s' % str(e)
            logger.error(msg)
        
    def process_item(self, item, spider):
        if spider.name=='author':
            try:
                cursor1=self.db.cursor()
                author_id=0
                if self.redis_conn.hexists('author',item['author_id']):
                    author_id=self.redis_conn.hget('author',item['author_id'])
                else:
                    relation_urls=','.join(item['relation_urls'])
                    sql="insert into `author` (`name`,`dynasty`,`author_url`,`faceimg`,`descp`,`pinyin`,`relation_urls`) values(%s,%s,%s,%s,%s,%s,%s)"
                    cursor1.execute(sql,[item['author'],item['dynasty'],item['author_url'],item['faceimg'],item['author_desc'],item['pinyin'],relation_urls])
                    author_id=str(cursor1.lastrowid)
                    self.redis_conn.hsetnx('author',item['author_id'],author_id)
                if item['relation_urls']:
                    sql="insert into `author_relation` (`author_id`,`title`,`description`,`created`,`editor`,`view_url`) values(%s,%s,%s,%s,%s,%s)"
                    created=int(time.time())
                    cursor1.execute(sql,[author_id,item['title'],item['content'],created,item['editor'],item['view_url']])
            except mysql.connector.Error as e:
                msg=u'author_url:%s 写入数据失败:%s' % (item['author_url'],e)
                logger.error(msg)
                cursor1.close()
            finally:
                cursor1.close()
            return item
        else:
            return item

class ArticlePipeline(object):
    def __init__(self):
        mysql_db=settings.MYSQL_DB
        try:
            self.db = mysql.connector.connect(host=mysql_db['host'],user=mysql_db['user'], password=mysql_db['password'], database=mysql_db['database'],charset=mysql_db['charset'])
        except mysql.connector.Error as e:
            msg=u'数据库连接失败:%s' % str(e)
            logger.error(msg)
        try:
            pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
            self.redis_conn = redis.Redis(connection_pool=pool)
        except redis.RedisError as e:
            msg='redis connect error %s' % str(e)
            logger.error(msg)
    
    def process_item(self, item, spider):
        if spider.name=='songs':
            try:
                cursor1=self.db.cursor()
                author_id=0
                keys=lazy_pinyin(item['author']+'_'+item['dynasty'])
                key=''.join(keys)
                kwd=''
                if self.redis_conn.hexists('author',item['author_id']):
                    kwd=item['author_id']
                elif self.redis_conn.hexists('author',key):
                    kwd=key
                if kwd!='':
                    author_id=self.redis_conn.hget('author',kwd)
                else:
                    sql="insert into `author` (`name`,`dynasty`,`pinyin`) values(%s,%s,%s)"
                    cursor1.execute(sql,[item['author'],item['dynasty'],item['pinyin']])
                    author_id=str(cursor1.lastrowid)
                    self.redis_conn.hsetnx('author',key,author_id)
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
            return item
        else:
            return item
