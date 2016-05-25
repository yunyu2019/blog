#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/evil.html
"""
def transfer(strs):
    return ''.join(byte if ' '<byte<'~' else '.' for byte in strs)
fp=open('evil2.jpg','rb')
jpg_cont=fp.read(16)
fp.close()
fp1=open('../09/9.png','rb')
png_cont=fp1.read(16)
fp1.close()
fp2=open('evil2.gfx','rb')
gfx_cont=fp2.read()
fp2.close()
fp3=open('bert.gif','rb')
gif_cont=fp3.read(16)
fp3.close()

print transfer(jpg_cont)
print transfer(png_cont)
print transfer(gif_cont)
print transfer(gfx_cont)
print transfer(gfx_cont[0:80:5])
print transfer(gfx_cont[1:80:5])
print transfer(gfx_cont[2:80:5])
print transfer(gfx_cont[3:80:5])
print transfer(gfx_cont[4:80:5])
"""
fp=open('evil2.gfx','rb')
cont=fp.read()
fp.close()
ls=zip([cont[0::5],cont[1::5],cont[2::5],cont[3::5],cont[4::5]],['0.jpg','1.png','2.gif','3.png','4.jpg'])
for content,filename in ls:
    fp=open(filename,'wb')
    fp.write(content)
    fp.close()
    