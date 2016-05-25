#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Date    : 2016-05-10 17:54:36
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @descp   : 练习wav模块获取wav文件信息

import wave
import struct

songs=wave.open('indian.wav','rb')
print songs.getparams()
channels=songs.getnchannels()              #声道数       1
total_frames=songs.getnframes()            #总帧数       55788 
sample_rate=songs.getframerate()           #采样率       11025
sample_width=songs.getsampwidth()          #每帧的数据量(字节) 2
last_time=1.0*total_frames/sample_rate
data_size=sample_width*total_frames*channels
bites_per_frame=8*sample_width*channels
bites_per_seconds=sample_rate*sample_width*channels
print '播放时长(s):%s' % last_time
print '数据大小(B):%s' % data_size
print '文件大小(B):%s' % (data_size+44)
print '每帧位数(bit):%s' % bites_per_frame
print '每秒数据量(B):%s' % bites_per_seconds
print '码率:%s' % (bites_per_seconds*8)
