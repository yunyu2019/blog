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
        html ='''<html lang="zh-cn">
        <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <link href="/static/default.css" rel="stylesheet">
        <link href="/static/github.css" rel="stylesheet">
        </head>
        <body>
        %s
        </body>
        </html>'''
        ret = markdown.markdown(mdstr,extensions=self.exts)
        return html % ret

    def filterDir(self,dir):
        flag=False
        for x in self.exclude:
            sub='{0}{1}'.format(os.sep,x)
            if dir.find(sub)>0:
                flag=True
                break
        
        return flag

    def getMds(self):
        for dirs,paths,files in os.walk(self.source):
            flag=self.filterDir(dirs)
            if flag:
                continue

            if isinstance(files,list):
                for x in files:
                    if self.filters:
                        if x.endswith(tuple(self.filters)):
                            yield (dirs,x)
                    else:
                        yield (dirs,x)

            else:
                yield (dirs,files)

    def writeHtml(self,file):
        dest_dir=file[0].replace(self.source,self.output)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        dest_f=file[1].replace('.md','.html')
        dest_file=os.path.join(dest_dir,dest_f)
        sf=os.sep.join(file)
        with open(sf,'r',encoding="utf-8") as fp,open(dest_file,'w+',encoding='utf-8') as f:
            cont=fp.read()
            cont=re.sub('\((.*)\.md\)','(\\1.html)',cont)
            html=self.md2html(cont)
            f.write(html)

        print('{0} success'.format(sf))

    def run(self):
        if not os.path.isdir(self.source):
            print('{0} is not real directory'.format(source))
            sys.exit()

        if not os.path.isdir(self.output):
            os.makedirs(self.output)

        num=0
        for x in self.getMds():
            self.writeHtml(x)
            num+=1

        print('find {0} markdown files'.format(num))
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

