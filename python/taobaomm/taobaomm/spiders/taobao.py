# -*- coding: utf-8 -*-
import os
import scrapy
import re
import urlparse
import logging
from functions import *
from pypinyin import lazy_pinyin
from scrapy.selector import Selector
from taobaomm.settings import LOG_FILE
from taobaomm.items import MMItem

logger=logging.getLogger('taobaomm')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.ERROR)
log_path=os.path.dirname(LOG_FILE)+'/error.log'
handler=logging.FileHandler(log_path,mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)

class TaobaoSpider(scrapy.Spider):
    name='taobao'
    allowed_domains=['mm.taobao.com']
    start_urls = [
        "https://mm.taobao.com/json/request_top_list.htm?page=%d" % d for d in range(1,5)
    ]
    
    def parse(self,response):
        curr_url=response.url
        curr_query=urlparse.urlparse(curr_url)
        curr_params=urlparse.parse_qs(curr_query.query)
        page=curr_params['page'][0]
        hxs = Selector(response)
        lists=hxs.xpath('//div[@class="list-item"]')
        for v in lists:
            try:
                    user=MMItem()
                    names=v.css('.lady-name').re('<a.*?href="(.*?)".*?>(.*?)</a>')
                    tags=v.css('.pic-word  em:nth-child(1)').extract()
                    faces=v.css('.lady-avatar').re('<a.*?href="(.*?)".*?<img src="(.*?)">*?')
                    descps=v.css('.description').extract()
                    user['name']=names[1].strip()
                    user['profile_url']='https:'+names[0].strip()
                    user['home_url']   ='https:'+faces[0]
                    user['faceimg']    ='https:'+faces[1]
                    user['age']        =v.css('.top strong::text').extract()[0]
                    user['city']       =v.css('.top span::text').extract()[0]
                    user['tags']       =filterHtml(tags[0]) if tags else ''
                    user['fans']       =v.css('.pic-word strong::text')[1].extract()
                    user['big_img']    ='https:'+v.css('.w610 img::attr(data-ks-lazyload)').extract()[0]
                    user['integral']   =v.css('.popularity dd::text').extract()[1].strip()
                    user['rates']      =v.css('.info-detail li strong::text')[1].extract()
                    user['imgnums']    =v.css('.info-detail li strong::text')[2].extract()
                    user['signnum']    =v.css('.info-detail li strong::text')[3].extract()
                    user['descp']      =filterHtml(descps[0]) if descps else ''
                    result=urlparse.urlparse(user['profile_url'])
                    params=urlparse.parse_qs(result.query)
                    profile_url='https://mm.taobao.com/self/info/model_info_show.htm?user_id='+params['user_id'][0]
                    yield scrapy.Request(profile_url,callback=self.parse_profile,meta={'item':user,'page':page},errback=self.catchError)
            except Exception, e:
                    msg=u"urls:%s message:%s" % (curr_url,str(e))
                    logger.error(msg)
    def catchError(self,response):
        item=response.meta['item']
        page=response.meta['page']
        msg=u'抓取第'+page+u'页 用户:'+item['name']+u'信息失败'
        logger.error(msg) 
            
    def parse_profile(self,response):
        hxs=Selector(response)
        item=response.meta['item']
        page=response.meta['page']
        cont=hxs.xpath('//div[@class="mm-p-info mm-p-base-info"]')
        ls=cont.xpath('ul/li/span').extract()
        ls1=cont.xpath('ul/li/p').extract()
        lists=map(filterHtml,ls)
        profiles=map(filterHtml,ls1)
        exprince=hxs.xpath('//div[@class="mm-p-info mm-p-experience-info"]/p').extract()
        item['nicename']=lists[0].strip()
        item['borthday']=lists[1].replace(u'\xa0','')
        item['job']     =lists[3].strip(u'型')
        item['blood']   =lists[4].strip(u'型')
        item['school']  =''
        item['specialty']  =''
        if lists[5]!='':
            m=re.split(u'\xa0{2,}',lists[5])
            if len(m)>1:
                item['school']  =m[0]
                item['specialty']  =m[1]
        item['style']   =lists[6].strip()
        item['height']  =profiles[0].strip('CM')
        item['weight']  =profiles[1].strip('KG')
        item['solid']   =profiles[2].strip()
        item['bar']     =bar(profiles[3])
        item['shoes']   =profiles[4].strip(u'码')
        item['exprince']=filterHtml(exprince[0])
        left_img=hxs.xpath('//div[@class="mm-p-modelCard"]/a/img/@src').extract()
        item['life_img']='https:'+left_img[0] if left_img else ''
        item['image_urls']=[item['faceimg'],item['big_img'],item['life_img']]
        username=lazy_pinyin(item['nicename'])
        item['pinyin']=''.join(username)
        yield item
