#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-09-06 14:30:51
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : The document description

import os
import sys
import re
import argparse
import markdown

class Mk2Html(object):
    """docstring for Mk2Html"""
    def __init__(self,**kw):
        self.exts= ['markdown.extensions.extra', 'markdown.extensions.codehilite','markdown.extensions.tables','markdown.extensions.toc']
        self.source=kw.get('source','')
        self.exclude=kw.get('exclude',[])
        self.filters=kw.get('filters',[])
        self.output=kw.get('output','')

    def md2html(self,mdstr):
        html ='''
        <html lang="zh-cn">
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <link href="/static/default.css" rel="stylesheet">
        <link href="/static/github.css" rel="stylesheet">
        </head>
        <body>
        %s
        </body>
        </html>
        '''
        ret = markdown.markdown(mdstr,extensions=self.exts)
        return html % ret

    def filterDir(self,dir):
        flag=False
        for x in self.exclude:
            sub='/{0}'.format(x)
            if dir.find(sub)>0:
                flag=True
                break
        
        return flag

    def getMds(self):
        s=[]
        for i in os.walk(self.source):
            dir=i[0].replace('\\','/')
            flag=self.filterDir(dir)
            if flag:
                continue

            if type(i[2]==list):
                for x in i[2]:
                    if self.filters:
                        if x.split('.')[-1] in self.filters:
                            s.append((dir,x))
                    else:
                        s.append((dir,x))

            else:
                s.append((dir,i[2]))

        return s

    def writeHtml(self,file):
        sf='/'.join(file)
        with open(sf,'r',encoding="utf-8") as fp:
            cont=fp.read()

        cont=re.sub('\((.*)\.md\)','(\\1.html)',cont)
        dest_dir=file[0].replace(self.source,self.output)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        dest_f=file[1].replace('.md','.html')
        dest_file=os.path.join(dest_dir,dest_f)
        with open(dest_file,'w+',encoding='utf-8') as f:
            html=self.md2html(cont)
            f.write(html)

        print('{0} success'.format(sf))

    def run(self):
        if not os.path.isdir(self.source):
            print('{0} is not real directory'.format(source))
            sys.exit()
    
        m=self.getMds()
        num=len(m)
        if num<1:
            print('no markdown file to transfer')
            sys.exit()

        print('find {0} markdown files'.format(num))
        if not os.path.isdir(self.output):
            os.makedirs(self.output)

        for i in m:
           self.writeHtml(i)

        print('transfer over')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='transfer markdown file to html file',prog='md2html')  
    parser.add_argument('-s','--source',required=True,type=str,help='source markdown file path')
    parser.add_argument('-o','--output',required=True,type=str,help='the output file path')
    parser.add_argument('-e','--exclude',nargs='*',help='the exclude file path')
    parser.add_argument('-c','--filter',nargs='*',help='choose extensions file')
    args = parser.parse_args()
    source = args.source  
    output = args.output
    exclude=args.exclude
    filters=args.filter
    kw={"source":source,"output":output,"exclude":exclude,"filters":filters}
    mk=Mk2Html(**kw)
    mk.run()

