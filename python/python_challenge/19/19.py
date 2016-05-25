#/usr/bin/python
#-*- coding: utf-8 -*-
#note:
#http://www.pythonchallenge.com/pc/hex/bin.html
import re
import wave
import email
import base64
import requests

req=requests.get('http://www.pythonchallenge.com/pc/hex/bin.html',auth=('butter','fly'))
cont=req.text
rule=re.compile('<!--\n(.*)-->',re.S)
emails=re.findall(rule,cont)
fp=open('email.txt','w')
fp.write(emails[0])
fp.close()

"""
#生成indian.wav的方法一:
rule=re.compile('base64\n{2}(.*)\n{2}',re.S)
m=re.search(rule1,cont)
res=base64.decodestring(m.group(1))
fp=open('indian.wav','wb')
fp.write(res)
fp.close()
"""

#利用email附件生成indian.wav的方法二
mail=email.message_from_file(open('email.txt'))
print mail.items()
print '邮件内容: %s' % mail.preamble
for part in mail.walk():
    if part.get_content_maintype()=='audio':
        file_name=part.get_filename()
        data=part.get_payload(decode=True)
        fp=open(file_name,'wb')
        fp.write(data)
        fp.close()

"""
#生成转换后的wav文件的方法一:
songs=wave.open('indian.wav','rb')
wo=wave.open('output.wav','wb')
params=songs.getparams()
wo.setparams(params)
nframes=songs.getnframes() #总帧数
for i in range(nframes):
	per_frame=songs.readframes(1)[::-1]
	wo.writeframes(per_frame)
songs.close()
wo.close()
"""

#生成转换后的wav文件的方法二:
fp=open('indian.wav','rb')
data=fp.read()
fp.close()
file_head,file_data=data[:44],data[44:]
wav_data=zip(file_data[::2],file_data[1::2])
cont=''.join(b2+b1 for b1,b2 in wav_data)
fp=open('output.wav','wb')
fp.write(file_head)
fp.write(cont)
fp.close()