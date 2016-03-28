# -*- coding: utf-8 -*-

import re
import redis
import codecs
import scrapy
import logging
import urlparse
import traceback
from songs.items import *
from pypinyin import lazy_pinyin
from scrapy.selector import Selector


logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
handler=logging.FileHandler('/home/www/songs/error.log',mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class SongsSpider(scrapy.Spider):
    name='songs'
    allowed_domains=['so.gushiwen.org']
    start_urls = [
        "http://so.gushiwen.org/type.aspx?p=%d" % d for d in range(1,10)
    ]

    def __init__(self, *a, **kw):
        super(SongsSpider, self).__init__(*a, **kw)
        try:
             pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
             self.redis_conn = redis.Redis(connection_pool=pool)
        except redis.RedisError as e:
             msg='redis connect error %s' % str(e)
             logger.error(msg)

    def parse(self,response):
        curr_url=response.url
        curr_query=urlparse.urlparse(curr_url)
        curr_params=urlparse.parse_qs(curr_query.query)
        page=curr_params['p'][0]
        hxs = Selector(response)
        lists=hxs.xpath('//div[@class="sons"]')
        for v in lists:
            try:
                    song=SongsItem()
                    author_url=v.xpath('a[1]/@href').extract()
                    author_url=author_url[0] if author_url  else ''
                    view_url=v.xpath('p[1]/a/@href').extract()[0]
                    title=v.xpath('p[1]/a/text()').extract()[0]
                    comments=v.xpath('p[2]/text()').extract()[0]
                    m=re.search('(\d\.?\d).*?(\d+)',comments)
                    point=0
                    nums=0
                    author_id=0
                    grs=m.groups()
                    if len(grs)>1:
                        point=grs[0]
                        nums=grs[1]
                    if author_url!='':
                        m1=re.search('(\d+)',author_url)
                        author_id=m1.group(1)
                    song['author_id']=author_id
                    song['author_url']=author_url
                    song['view_url']  =view_url
                    song['title']     =title
                    song['comment_nums']      =nums
                    song['point']     =point
                    view_url='http://so.gushiwen.org'+view_url
                    yield scrapy.Request(view_url,callback=self.parse_song,meta={'item':song,'page':page},errback=self.catchError)
            except:
                    fp=codecs.open('/home/www/songs/error.log','a','utf-8')
                    traceback.print_exc(file=fp)
    def catchError(self,response):
        item=response.meta['item']
        page=response.meta['page']
        msg=u'抓取第'+page+u'页 用户:'+item['name']+u'信息失败'
        logger.error(msg) 
            
    def parse_song(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=response.meta['page']
        cont=hxs.xpath('//div[@class="son2"]')[1]
        dynasty=cont.xpath('p[1]/text()').extract()[0].strip()
        author_temp=cont.xpath('p[2]/a/text()').extract()
        author=author_temp[0] if author_temp else cont.xpath('p[2]/text()').extract()[0]
        strs=cont.extract()
        compiles=re.compile(r'</span></p>(.*)?.*?</div>',re.S)
        m=re.search(compiles,strs)
        content=m.group(1).strip()
        item['dynasty']=dynasty
        item['author'] =author
        item['content']=content
        flag=item['author_url']!='' and not self.redis_conn.hexists('author',item['author_id'])
        if flag:
            author_url='http://so.gushiwen.org'+item['author_url']
            yield scrapy.Request(author_url,callback=self.parse_author,meta={'item':item,'page':page},errback=self.catchError)
        else:
            
            if not self.redis_conn.hexists('author',item['author_id']):
                item['faceimg']=''
                item['author_desc']='' 
                keys=lazy_pinyin(item['author']+'_'+item['dynasty'])
                key=''.join(keys)
                item['pinyin']=key.split('_')[0]
                self.redis_conn.hsetnx('author',key,0)
            yield item
    def parse_author(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=response.meta['page']
        cont=hxs.xpath('//div[@class="son2"]')[1]
        faceimg=cont.xpath('div/img/@src').extract()[0].strip()
        strs=cont.extract()
        compiles=re.compile(r'<img.*?>.*?</div>(.*)?</div>',re.S)
        m=re.search(compiles,strs)
        author_desc=m.group(1).strip()
        item['faceimg']=faceimg
        item['author_desc']=author_desc
        songname=lazy_pinyin(item['author'])
        item['pinyin']=''.join(songname)
        self.redis_conn.hsetnx('author',item['author_id'],0)
        return  item
