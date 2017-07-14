#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-14 15:41:18
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : The document description

import jieba
import codecs
from os import path
from wordcloud import WordCloud

class Cloud(object):
    """docstring for Cloud"""
    def __init__(self,source,dist,img=None):
        super(Cloud, self).__init__()
        d = path.dirname(__file__)
        self.root=d
        self.source = path.join(d,source)
        self.dist=path.join(d,dist)
        img_name=img if img else 'cn_clound.png'
        self.img=path.join(d,img_name)
    
    def readCont(self):
        print('begin read content')
        fp=codecs.open(self.source,'r',encoding='utf-8')
        cont=fp.readlines()
        fp.close()
        print('read content successful')
        return cont[0]

    def create_dict(self,cont):
        import jieba.posseg as pseg
        print('begin create dict file')
        words=pseg.cut(cont)
        tags=set()
        for w in words:
            if w.flag == 'x':
                continue
            tags.add((w.word,w.flag))

        with codecs.open(self.dist,'w+',encoding='utf-8') as fp:
             for k,w in tags:
                 fp.write('{0} {1}\n'.format(k,w))

        print('create dict file successful,num is {0}'.format(len(tags)))

    def create_words(self,cont,stop=None):
        import jieba.analyse
        jieba.load_userdict(self.dist)
        print('begin analyse the key words')
        if stop:
            stopwords=path.join(self.root,stop)
            jieba.analyse.set_stop_words(stopwords)

        tags=jieba.analyse.extract_tags(cont,topK=100, withWeight=True, allowPOS=())
        print('analyse the key words successful,num is {0}'.format(len(tags)))
        return tags

    def create_cloud(self,words):
        print('begin create the cloud words images')
        font_path = path.join(self.root, 'fonts','msyh.ttf')
        wordcloud = WordCloud(max_font_size=40,font_path=font_path,background_color="gray").generate_from_frequencies(words)
        wordcloud.to_file(self.img)
        print('create the cloud words images successful')

    def run(self):
        cont=self.readCont()
        self.create_dict(cont)
        tags=self.create_words(cont,stop='stopwords.txt')
        if len(tags)>0:
            words=dict(tags)
            self.create_cloud(words)

if __name__ == '__main__':
    cloud=Cloud('content.txt','dict.txt')
    cloud.run()