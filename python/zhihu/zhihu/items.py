# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FollowItem(scrapy.Item):
    name=scrapy.Field()
    avatar=scrapy.Field()
    descp=scrapy.Field()
    view_url=scrapy.Field()
    data=scrapy.Field()

class PeopleItem(scrapy.Item):
	user_page=scrapy.Field()
	location=scrapy.Field()
	business=scrapy.Field()
	employment=scrapy.Field()
	position=scrapy.Field()
	education=scrapy.Field()
	education_extra=scrapy.Field()
	gender=scrapy.Field()
	content=scrapy.Field()
	answers=scrapy.Field()
	
class ActiveItem(scrapy.Item):
	url_page=scrapy.Field()
	starts=scrapy.Field()
	actives=scrapy.Field()
		
		

