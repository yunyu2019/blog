#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-22 17:26:26
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : instead songs_spider.py

import os
import re
import scrapy
import logging
import urlparse
from pypinyin import lazy_pinyin
from scrapy.http import Request
from songs.items import SongsItem
from songs.settings import LOG_FILE
from scrapy.selector import Selector

logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
log_path=os.path.dirname(LOG_FILE)+'/error.log'
handler=logging.FileHandler(log_path,mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class SingleSongSpider(scrapy.Spider):
    name='singlesong'
    allowed_domains=['so.gushiwen.org']
    start_urls = [
        "http://so.gushiwen.org/view_%d.aspx" % d for d in range(73049,73052)
    ]

    def parse(self,response):
        curr_url=response.url
        curr_query=urlparse.urlparse(curr_url)
        view_url=curr_query.path
        hxs = Selector(response)
        warp=hxs.xpath('//div[@class="shileft"]')
        if warp:
            song=SongsItem()
            song['view_url']  =view_url
            try:
                title=warp.xpath('div[@class="son1"]/h1/text()').extract()[0]
                son2=warp.xpath('div[@class="son2"]')
                temp=son2.css('.line1 *::text').extract()
                point=0
                comment_num=0
                if temp:
                    comment=temp[0].strip()
                    m=re.search('(\d+)',comment)
                    comment_num=m.group(1) if m else 0
                    point=temp[1].strip() if len(temp)>1 else 0
                dynasty=son2.xpath('p[1]/text()').extract()
                dynasty=dynasty[0] if dynasty else ''
                author_temp=son2.xpath('p[2]/a/text()').extract()
                author=author_temp[0] if author_temp else son2.xpath('p[2]/text()').extract()[0]
                author_name=lazy_pinyin(author)
                url_temp=son2.xpath('p[2]/a/@href')
                author_id=0
                if url_temp:
                    author_url=url_temp.extract()[0]
                    m1=re.search('(\d+)',author_url)
                    author_id=m1.group(1)
                strs=son2.extract()[0]
                compiles=re.compile(r'</span></p>(.*)?.*?</div>',re.S)
                m=re.search(compiles,strs)
                content=m.group(1).strip() if m.groups() else ''
                relation_urls=hxs.xpath('//div[@class="son5" and @id]/p[1]/a/@href').extract()
                song['title']     =title
                song['comment_nums']=comment_num
                song['point']     =point
                song['dynasty']=dynasty
                song['author'] =author
                song['content']=content
                song['pinyin']=''.join(author_name)
                song['author_id']=author_id
                song['relation_urls']=relation_urls if relation_urls else ''
                if relation_urls:
                    for i in relation_urls:
                        url='http://so.gushiwen.org'+i
                        yield Request(url,callback=self.parse_relation,meta={'item':song},errback=self.catchError)
                else:
                    yield song
            except Exception, e:
                msg=u"urls:%s message:%s" % (curr_url,str(e))
                logger.error(msg)
        else:
            msg=u"urls:%s message:%s" % (curr_url,'page not found')
            logger.error(msg)

    def parse_relation(self,response):
        item=response.meta['item']
        query=urlparse.urlparse(response.url)
        curr_url=query.path
        hxs = Selector(response)
        warp=hxs.xpath('//div[@class="shileft"]')
        try:
            shangxi=warp.xpath('div[@class="shangxicont"]')
            title=warp.xpath('div[@class="son1"]/h1/text()').extract()
            editor=shangxi.xpath('p[1]/text()').extract()
            temp=shangxi.xpath('p[not(@style)]').extract()
            rel_content=''
            if temp:
                rel_content=''.join(temp)
            else:
                shangxi=shangxi.extract()[0]
                rule=re.compile('<\/p>?(.*?)<p style=.*?',re.S)
                m=re.search(rule,shangxi)
                rel_content=m.group(1).strip() if m.groups() else ''
            item['rel_title']=title[0] if title else ''
            item['editor']=editor[0][3:] if editor else ''
            item['rel_content']=rel_content
            item['rel_url']=curr_url
        except Exception, e:
            msg=u"page:%s urls:%s message:%s" % (page,curr_url,str(e))
            logger.error(msg)
        return item

    def catchError(self,response):
        item=response.meta['item']
        msg=u"url:%s message:%s" %(response.url,'spider error')
        logger.error(msg)