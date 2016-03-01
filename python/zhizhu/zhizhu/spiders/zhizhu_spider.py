# -*- coding: utf-8 -*-

import scrapy
import re
import urlparse
import logging
import codecs
import traceback
from scrapy.selector import Selector
from zhizhu.items import *

logger=logging.getLogger('zhizhu')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
handler=logging.FileHandler('/home/www/zhizhu/error.log',mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ZhizhuSpider(scrapy.Spider):
    name='zhizhu'
    allowed_domains=['mm.taobao.com']
    start_urls = [
        "https://mm.taobao.com/json/request_top_list.htm?page=%d" % d for d in range(1001,1101)
    ]
    
    def parse(self,response):
        curr_url=response.url
        curr_query=urlparse.urlparse(curr_url)
        curr_params=urlparse.parse_qs(curr_query.query)
        page=curr_params['page'][0]
        if response.status==200: 
            hxs = Selector(response)
            lists=hxs.xpath('//div[@class="list-item"]')
            for v in lists:
                try:
                    user=ZhizhuItem()
                    names=v.css('.lady-name').re('<a.*?href="(.*?)".*?>(.*?)</a>')
                    tags=v.css('.pic-word  em:nth-child(1)').re('<em>(.*?)</em>')
                    faces=v.css('.lady-avatar').re('<a.*?href="(.*?)".*?<img src="(.*?)">*?')
                    compiles=re.compile('<p class="description">(.*?)</p>',re.S)
                    descps=v.css('.description').re(compiles)
                    user['name']=names[1].strip()
                    user['profile_url']='https:'+names[0].strip()
                    user['home_url']   ='https:'+faces[0]
                    user['faceimg']    ='https:'+faces[1]
                    user['age']        =v.css('.top strong::text').extract()[0]
                    user['city']       =v.css('.top span::text').extract()[0]
                    user['tags']       =tags[0]
                    user['fans']       =v.css('.pic-word strong::text')[1].extract()
                    user['big_img']    ='https:'+v.css('.w610 img::attr(data-ks-lazyload)').extract()[0]
                    user['integral']   =v.css('.popularity dd::text').extract()[1].strip()
                    user['rates']      =v.css('.info-detail li strong::text')[1].extract()
                    user['imgnums']    =v.css('.info-detail li strong::text')[2].extract()
                    user['signnum']    =v.css('.info-detail li strong::text')[3].extract()
                    user['descp']      =descps[0].strip()
                    result=urlparse.urlparse(user['profile_url'])
                    params=urlparse.parse_qs(result.query)
                    profile_url='https://mm.taobao.com/self/info/model_info_show.htm?user_id='+params['user_id'][0]
                    yield scrapy.Request(profile_url,callback=self.parse_profile,meta={'item':user,'page':page},errback=self.catchError)
                except:
                    fp=codecs.open('/home/www/zhizhu/error.log','a','utf-8')
                    traceback.print_exc(file=fp)
        else:
            msg=u'抓取第'+page+u'页信息失败'
            logger.error(msg)
    def catchError(self,response):
        item=response.meta['item']
        page=response.meta['page']
        if response.status!=200:
            msg=u'抓取第'+page+u'页 用户:'+item['name']+u'信息失败'
            logger.error(msg) 
            
    def parse_profile(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=response.meta['page']
        lists=hxs.css('.mm-p-base-info li span').re('<span>(.*?)</span>')
        profiles=hxs.css('.mm-p-base-info li p').re('<p>(.*?)</p>')
        compiles=re.compile('<p>(.*?)</p>',re.S)
        exprince=hxs.css('.mm-p-experience-info p').re(compiles)
        item['nicename']=lists[0].strip()
        item['borthday']=lists[1].strip()
        item['job']     =lists[3].strip(u'型')
        item['blood']   =lists[4].strip(u'型')	 
        item['school']  =lists[5].strip()
        item['style']   =lists[6].strip()
        item['height']  =profiles[0].strip('CM')
        item['weight']  =profiles[1].strip('KG')
        item['solid']   =profiles[2].strip()
        item['bar']     =profiles[3].strip()
        item['shoes']   =profiles[4].strip(u'码')
        item['exprince']=exprince[0].strip()
        item['life_img']='https:'+hxs.css('.mm-p-modelCard img::attr(src)').extract()[0]
        item['image_urls']=[item['faceimg'],item['big_img'],item['life_img']]
        yield item
