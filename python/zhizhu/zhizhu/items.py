# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhizhuItem(scrapy.Item):
    name=scrapy.Field()
    age=scrapy.Field()
    profile_url=scrapy.Field() 
    home_url=scrapy.Field()
    faceimg=scrapy.Field()
    tags=scrapy.Field()
    descp=scrapy.Field()
    city=scrapy.Field()
    imgnums=scrapy.Field()
    integral=scrapy.Field()
    fans=scrapy.Field()
    signnum=scrapy.Field()
    rates=scrapy.Field()
    integral=scrapy.Field()
    big_img=scrapy.Field()
    life_img=scrapy.Field()
    pinyin=scrapy.Field()
    nicename=scrapy.Field()
    borthday=scrapy.Field()
    job=scrapy.Field()
    blood=scrapy.Field()
    school=scrapy.Field()
    specialty=scrapy.Field()
    style=scrapy.Field()
    height=scrapy.Field()
    weight=scrapy.Field()
    bar=scrapy.Field()
    solid=scrapy.Field()
    shoes=scrapy.Field()
    exprince=scrapy.Field()
    image_urls=scrapy.Field()