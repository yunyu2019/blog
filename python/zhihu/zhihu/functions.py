#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-10-19 11:51:02
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : 
# @descp   : The document description

import re

def stripHtml(s):
	if s!='':
		s=s.strip().replace('\n','')
		rule=re.compile(r'<[^>]+>',re.S)
		s1=re.sub(rule,'',s)
		return s1
	return ''


	

