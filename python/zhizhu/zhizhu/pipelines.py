# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import os
from zhizhu import settings
import mysql.connector

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
            username=item['pinyin']
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
        
class MysqlsavePipeline(object):
    def __init__(self):
        mysql_db=settings.MYSQL_DB
        self.db = mysql.connector.connect(host=mysql_db['host'],user=mysql_db['root'], password=mysql_db['password'], database=mysql_db['database'],charset=mysql_db['charset'])
    
    def process_item(self, item, spider):
        cursor1=self.db.cursor()
        sql="insert into `user` (`name`,`age`,`profile_url`,`faceimg`,`tags`,`descp`,`city`,`imgnums`,`integral`,`fans`,`signnum`,`rates`,`model_img`,`big_img`,`life_img`,`pinyin`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor1.execute(sql,[item['name'],item['age'],item['home_url'],item['faceimg'],item['tags'],item['descp'],item['city'],item['imgnums'],item['integral'],item['fans'],item['signnum'],item['rates'],'',item['big_img'],item['life_img'],item['pinyin']])
        user_id=str(cursor1.lastrowid)
        sql1="insert into `profile` (`user_id`,`nicename`,`borthday`,`blood`,`school`,`style`,`height`,`weight`,`solid`,`bar`,`shoes`,`exprince`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor1.execute(sql1,[user_id,item['nicename'],item['borthday'],item['blood'],item['school'],item['style'],item['height'],item['weight'],item['solid'],item['bar'],item['shoes'],item['exprince']])
        cursor1.close()
        return item
