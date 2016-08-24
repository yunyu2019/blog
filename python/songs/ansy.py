#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-24 14:05:21
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import re
import sys
import json
import codecs

def ansyArticle(data):
	"""分析错误日志"""
	ids=[]
	with open(data,'r') as fp:
		i=0
		for line in fp.readlines():
			i+=1
			if i%5==1:
				m=re.search('view_(\d+)\.aspx',line)
				ids.append(m.group(1))
			else:
				continue
	return ids

def ansyAuthor(data):
	"""分析json文件"""
	ids=[]
	with open(data,'r') as fp:
		for line in fp.readlines():
			item=json.loads(line)
			if item['author_id'] not in ids:
				ids.append(int(item['author_id']))
	
	return ids,max(ids)


if __name__ == '__main__':
	data=sys.argv[1]
	records=ansyArticle(data)
	cont={"article":records}
	fp=codecs.open('record.log', 'a', encoding='utf-8')
	line = json.dumps(cont, ensure_ascii=False) + "\n"
	fp.write(line)
	fp.close()
	"""
	ids,max_id=ansyAuthor(data)
	print ids,max_id
	"""
