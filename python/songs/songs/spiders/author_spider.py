# -*- coding: utf-8 -*-

import os
import re
import redis
import scrapy
import logging
import urlparse
from pypinyin import lazy_pinyin
from songs.items import AuthorItem
from songs.settings import LOG_FILE
from scrapy.selector import Selector

logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
log_path=os.path.dirname(LOG_FILE)+'/error.log'
handler=logging.FileHandler(log_path,mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AuthorSpider(scrapy.Spider):
    name='author'
    allowed_domains=['so.gushiwen.org']
    start_urls = [
        "http://so.gushiwen.org/authors/Default.aspx?p=%d" % d for d in range(1,3)
    ]

    def parse(self,response):
        curr_url=response.url
        curr_query=urlparse.urlparse(curr_url)
        curr_params=urlparse.parse_qs(curr_query.query)
        page=curr_params['p'][0]
        hxs = Selector(response)
        lists=hxs.xpath('//div[@class="sonsauthor"]')
        for v in lists:
            try:
                    author=AuthorItem()
                    author_urls=v.xpath('a[1]/@href').extract()
                    if author_urls:
                        author_url=author_urls[0]
                    else:
                        author_urls=v.xpath('p[1]/a/@href').extract()
                        author_url=author_urls[0] if author_urls else ''
                    thumb_img=v.xpath('a[1]/img/@src').extract()
                    thumb_img=thumb_img[0] if thumb_img else ''
                    title=v.xpath('p[1]/a/text()').extract()[0]
                    dynasty=''
                    dynasty_temp=v.xpath('p[2]/text()').extract()
                    if dynasty_temp:
                        dynasty=dynasty_temp[0].strip()
                        dynasty=dynasty[3:]
                    author_id=0
                    if author_url!='':
                        m1=re.search('(\d+)',author_url)
                        author_id=m1.group(1)
                    author['author']     =title
                    author['faceimg']   =thumb_img
                    author['author_id'] =author_id
                    author['author_url']=author_url
                    author['dynasty']=dynasty
                    author['page']=page
                    author_name=lazy_pinyin(author['author'])
                    author['pinyin']=''.join(author_name)
                    if author_url:
                        view_url='http://so.gushiwen.org'+author_url
                        yield scrapy.Request(view_url,callback=self.parse_author,meta={'item':author},errback=self.catchError)
                    else:
                        yield author
            except Exception, e:
                    msg=u"page:%s urls:%s message:%s" % (page,curr_url,str(e))
                    logger.error(msg)
    def catchError(self,response):
        item=response.meta['item']
        page=item['page']
        msg=u"page:%s message:%s" %(page,response.url)
        logger.error(msg) 
            
    def parse_author(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=item['page']
        cont=hxs.xpath('//div[@class="son2"]')[1]
        author_desc=''
        m=cont.xpath('*/text()').extract()
        if m:
        	m1=[i.strip() for i in m if i.strip()]
        	if m1:
        		author_desc=''.join(m1)
        	else:
        		s=cont.xpath('text()').extract()
        		s1=[i.strip() for i in s if i.strip()]
        		author_desc=s1[0]
        else:
        	s=cont.xpath('text()').extract()
        	author_desc=s[0].strip()
        relation_urls=hxs.xpath('//div[@class="son5"]/p[1]/a/@href').extract()
        item['author_desc']=author_desc  
        item['relation_urls']=relation_urls if relation_urls else ''
        if relation_urls:
            for i in relation_urls:
                view_url='http://so.gushiwen.org'+i
                yield scrapy.Request(view_url,callback=self.parse_author_profile,meta={'item':item},errback=self.catchError)
        else:
            yield item
        
    def parse_author_profile(self,response):
        item=response.meta['item']
        page=item['page']
        query=urlparse.urlparse(response.url)
        curr_url=query.path
        hxs=Selector(response)
        cont=hxs.xpath('//div[@class="shileft"]')
        try:
            title =cont.xpath('./div[@class="son1"]/h1/text()').extract()[0].strip()
            editor=cont.xpath('./div[@class="shangxicont"]/p[1]/text()').extract()
            strs=cont.xpath('./div[@class="shangxicont"]').extract()[0]
            rule=re.compile('<div class="shangxicont".*?</p>?(.*)?.*<p style=".*?color:#919090.*?',re.S)
            m=re.search(rule,strs)
            content=m.group(1).strip()
            editor=editor[0] if editor else ''
            item['title']=title
            item['editor']=editor
            item['content']=content
            item['view_url']=curr_url
        except Exception, e:
            msg=u"page:%s urls:%s message:%s" % (page,response.url,str(e))
            logger.error(msg)
        return item
        
