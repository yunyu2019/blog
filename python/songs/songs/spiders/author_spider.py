# -*- coding: utf-8 -*-

import re
import redis
import codecs
import scrapy
import logging
import urlparse
import traceback
from songs.items import AuthorItem
from pypinyin import lazy_pinyin
from scrapy.selector import Selector


logger=logging.getLogger('songs')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
handler=logging.FileHandler('/home/www/songs/error.log',mode='a',encoding='utf-8')
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
                    author_url=v.xpath('a[1]/@href').extract()
                    author_url=author_url[0] if author_url  else ''
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
                    view_url='http://so.gushiwen.org'+author_url
                    yield scrapy.Request(view_url,callback=self.parse_author,meta={'item':author,'page':page},errback=self.catchError)
            except:
                    fp=codecs.open('/home/www/songs/error.log','a','utf-8')
                    traceback.print_exc(file=fp)
    def catchError(self,response):
        item=response.meta['item']
        page=response.meta['page']
        msg=u'抓取第%s页 用户:%s信息失败' %(page,item['author'])
        logger.error(msg) 
            
    def parse_author(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=response.meta['page']
        cont=hxs.xpath('//div[@class="son2"]')[1]
        strs=cont.extract()
        compiles=re.compile(r'<img.*?>.*?</div>(.*)?</div>',re.S)
        m=re.search(compiles,strs)
        author_desc=m.group(1).strip()
        item['author_desc']=author_desc
        author_name=lazy_pinyin(item['author'])
        item['pinyin']=''.join(author_name)
        relation_urls=hxs.xpath('//div[@class="son5"]/p[1]/a/@href').extract()
        item['relation_urls']=relation_urls if relation_urls else ''
        if relation_urls:
            for i in relation_urls:
                view_url='http://so.gushiwen.org'+i
                yield scrapy.Request(view_url,callback=self.parse_author_profile,meta={'item':item,'page':page,'curr_url':i},errback=self.catchError)
        else:
            yield item
        
    def parse_author_profile(self,response):
        item=response.meta['item']
        page=response.meta['page']
        curr_url=response.meta['curr_url']
        hxs=Selector(response)
        cont=hxs.xpath('//div[@class="shileft"]')
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
        return item
        
