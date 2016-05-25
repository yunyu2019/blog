#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-24 16:11:37
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : http://www.pythonchallenge.com/pc/rock/arecibo.html

import os
import Image
import requests

def downfile(url):
    req=requests.get(url,auth=('kohsamui','thailand'))
    filename=os.path.basename(url)
    fp=open(filename,'wb')
    fp.write(req.content)
    fp.close()
    return filename

def loadfile(filename):
    """读取文件内容"""
    data=dict()
    with open(filename,'r') as fp:
        for line in fp:
            if line.startswith('\n'):
                continue
            elif line.startswith('#'):
                index=line.split()[1]
                data[index]=list()
            else:
                cont=map(int,line.split())
                data[index].append(cont)
        return data['Dimensions'],data['Horizontal'],data['Vertical']

def candidata(data,maxlen):
    """得到所有可能的排序列表"""
    candi=[]
    length=len(data)
    num=maxlen-(length-1)-sum(data) #空格数量
    for i in range(num+1):
        cans = 'O'*i + '#'*data[0]
        if length==1:
            tail = 'O'*(maxlen-len(cans))
            candi.append(cans+tail)
        else:
            tail = ['O'+j for j in candidata(data[1:], maxlen-len(cans)-1)]
            candi.extend([cans + j for j in tail])
    return candi

def fillinit(w,h,hdata,vdata):
    """初始化所有可能的排序集合"""
    posbH = []
    posbV = []
    for i in range(h):
        posbH.append(candidata(hdata[i],w))
    for i in range(w):
        posbV.append(candidata(vdata[i],h))
    return posbH, posbV

def checkpos(data,pos,flag):
    """根据特定位置的字符过滤所有的可能的排序集合"""
    ndata=[a for a in data if a[pos]==flag]
    return ndata

def solver(url,filename):
    file_name=downfile(url)
    size,hdata,vdata=loadfile(file_name)
    w,h=size[0][0],size[0][1]
    posbH,posbV=fillinit(w,h,hdata,vdata)
    
    count = 0
    nums = w*h
    result = []
    
    for i in range(w):
        result.append(['?' for j in range(h)])
    
    while count<nums:
        for x in range(w):
            i=posbH[x]
            m=''
            if m=='done':
                continue
            elif len(i)==1:
                for y in range(h):
                    if result[x][y] == '?':
                        count+=1
                        result[x][y] = i[0][y]
                        posbV[y] = checkpos(posbV[y],x,i[0][y])
                m='done'
            else:
                for y in range(h):
                    if result[x][y] != '?':
                        continue
                    for k in i[1::]:
                        if k[y]!=i[0][y]:
                            break
                    else:
                        count+=1
                        result[x][y] = i[0][y]
                        posbV[y] = checkpos(posbV[y],x,i[0][y])
                        
        for y in range(h):
            i=posbV[y]
            m=''
            if m=='done':
                continue
            elif len(i)==1:
                for x in range(w):
                    if result[x][y] == '?':
                        count+=1
                        result[x][y] = i[0][x]
                        posbH[x] = checkpos(posbH[x],y,i[0][x])
                m='done'
            else:
                for x in range(w):
                    if result[x][y] != '?':
                        continue
                    for k in i[1::]:
                        if k[x]!=i[0][x]:
                            break
                    else:
                        count+=1
                        result[x][y] = i[0][x]
                        posbH[x] = checkpos(posbH[x],y,i[0][x])
        
        s = []
        for i in range(w):
            s.extend([1 if j=='O' else 0 for j in result[i]])
        
        img=Image.new('1',(w,h))
        img.putdata(s)
        img.save(filename)
    
if __name__ == '__main__':
    #solver('http://www.pythonchallenge.com/pc/rock/warmup.txt','warmup.png')
    solver('http://www.pythonchallenge.com/pc/rock/up.txt','32.png')
    """
    http://www.pythonchallenge.com/pc/rock/python.html==>"Free" as in "Free speech", not as in "free... ==>Free As In Speech, But Not Free As In Beer
    """
    
    