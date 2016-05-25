#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
#方法一:
def maketrans(message):
    s=''
    for i in message:
        if i.isalpha():
            temp=ord(i)+2
            z=ord('z')
            if temp > z:
                temp-=26
            s+=chr(temp)
        else:
            s+=i
    return s

#方法二(比方法一高效)
def maketrans(message):
    s=''
    table1='abcdefghijklmnopqrstuvwxyz'
    table2='cdefghijklmnopqrstuvwxyzab'
    dit=dict(zip(table1,table2)) #{'a':'c','b':'d',...'y':'a','z':'b'}
    for i in message:
        if i in table1:
            s+=dit[i]
        else:
            s+=i
    return s
    
mess="g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."   
message=maketrans(mess)
print message   
"""
#方法三
import string
mess="g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
az=string.ascii_lowercase
table=string.maketrans(az,az[2:]+az[:2])
message=mess.translate(table)
print message
ls='map'
old_url='http://www.pythonchallenge.com/pc/def/map.html'
new_url=old_url.replace(ls,ls.translate(table))
print new_url