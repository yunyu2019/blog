#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-13 17:29:16
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : The document description

import jieba
from jieba import analyse
from os import path
from wordcloud import WordCloud,STOPWORDS

d = path.dirname(__file__)
font_path = path.join(d, 'fonts','msyh.ttf')
text='我跟朋友说起中国有嘻哈没买版权的时候她很震惊，再指路去看南韩关于中餐厅抄袭报道的评论时，大家躺平任嘲苦笑了之，上次网络文学审查的玩意，没有主旋律扣分是抄袭的五倍，楚乔传夸张到直接剪进暮光之城的镜头，至今没有看到片方任何回应。说实话，在你国谈版权就是个笑话。'
jieba.load_userdict('user_dict.txt')
tags=analyse.extract_tags(text, topK=20, withWeight=True, allowPOS=('v','n','ns','nz','nr'))
words=dict(tags)
wordcloud = WordCloud(font_path=font_path,background_color="white",stopwords=STOPWORDS).generate_from_frequencies(words)
wordcloud.to_file('cn.png')
