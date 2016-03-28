# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SongsItem(scrapy.Item):
    author_url=scrapy.Field()
    author_id=scrapy.Field()
    title=scrapy.Field()
    dynasty=scrapy.Field() 
    view_url=scrapy.Field()
    faceimg=scrapy.Field()
    comment_nums=scrapy.Field()
    point=scrapy.Field()
    author=scrapy.Field()
    content=scrapy.Field()
    author_desc=scrapy.Field()
    pinyin=scrapy.Field()
