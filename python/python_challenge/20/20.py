#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-10 10:33:17
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/hex/idiot2.html

import re
import base64
import zipfile
import requests

"""
start=1152983631
end=2123456789
message=[]
while start<end:
	headers = {
		    'Authorization': 'Basic ' + base64.b64encode('butter:fly'),
		    'Range': 'bytes=%s-%s' % (start,end)
	}
	req=requests.get('http://www.pythonchallenge.com/pc/hex/unreal.jpg',headers=headers)
	if 'content-range' in req.headers:
		cont_range=req.headers['content-range']
		m=re.search('(\d+)-(\d+)',cont_range)
		if m:
			start=int(m.group(2))+1
			message.append(req.text)
		else:
			break
	else:
		break  
print message

#正向：30203->30237->30284->30295->30313->30346(message:ok, invader. you are inside now.)->invader
#反向:2123456788(message:the password is your new nickname in reverse)->2123456743(message:and it is hiding at 1152983631)->1152983631
"""

start=1152983631
end=2123456789
headers = {
		    'Authorization': 'Basic ' + base64.b64encode('butter:fly'),
		    'Range': 'bytes=%s-%s' % (start,end)
}
req=requests.get('http://www.pythonchallenge.com/pc/hex/unreal.jpg',headers=headers)
cont=req.content
fp=open('unreal.zip','wb')
fp.write(cont)
fp.close()

zp=zipfile.ZipFile('unreal.zip')
passwd='invader'
zp.setpassword(passwd[::-1])
print zp.read('readme.txt')
