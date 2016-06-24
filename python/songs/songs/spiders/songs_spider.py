# -*- coding: utf-8 -*-

import re
import scrapy
import logging
import urlparse
from songs.items import SongsItem
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
        "http://so.gushiwen.org/type.aspx?p=%d" % d for d in range(1,3)
    ]

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
                song['view_url']  =view_url
                song['title']     =title
                song['comment_nums']      =nums
                song['point']     =point
                song['page']=page
                view_url='http://so.gushiwen.org'+view_url
                yield scrapy.Request(view_url,callback=self.parse_song,meta={'item':song},errback=self.catchError)
            except:
                    msg=u"page:%s urls:%s message:%s" % (page,curr_url,str(e))
                    logger.error(msg)
    def catchError(self,response):
        item=response.meta['item']
        page=item['page']
        msg=u"page:%s message:%s" %(page,response.url)
        logger.error(msg) 
            
    def parse_song(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=item['page']
        cont=hxs.xpath('//div[@class="son2"]')[1]
        dynasty=cont.xpath('p[1]/text()').extract()
        dynasty=dynasty[0] if dynasty else ''
        author_temp=cont.xpath('p[2]/a/text()').extract()
        author=author_temp[0] if author_temp else cont.xpath('p[2]/text()').extract()[0]
        strs=cont.extract()
        compiles=re.compile(r'</span></p>(.*)?.*?</div>',re.S)
        m=re.search(compiles,strs)
        content=m.group(1).strip()
        item['dynasty']=dynasty
        item['author'] =author
        item['content']=content
        author_name=lazy_pinyin(item['author'])
        item['pinyin']=''.join(author_name)
        return item
        
