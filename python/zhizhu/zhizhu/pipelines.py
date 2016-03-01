# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os
from pypinyin import lazy_pinyin
from zhizhu import settings

class ZhizhuPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

class MyImagesPipeline(object):
    def process_item(self,item,spider):
        images=item['image_urls']
        if len(images)>0:
            user=lazy_pinyin(item['nicename'])
            username=''
            for uls in user:
                username+=uls
            dir_path='%s/%s' % (settings.IMAGES_STORE,username)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for image_url in images:
                image_name = image_url.split('/')[-1]
                file_path = '%s/%s' % (dir_path, image_name)
                if os.path.exists(file_path):
                    continue
                with open(file_path, 'wb') as handle:
                    response = requests.get(image_url, stream=True)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
            return item
