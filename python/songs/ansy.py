#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-06-24 14:05:21
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import sys
import re

def ansyLog(data):
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

if __name__ == '__main__':
	data=sys.argv[1]
	records=ansyLog(data)
	print records
