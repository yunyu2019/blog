#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-07 16:35:27
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : The document description
# use Pillow

import os
import argparse
from PIL import Image

def isImage(filename):
    allows=('.jpg','.jpeg','.png')
    if  not filename.endswith(allows) or not os.path.isfile(filename):
	    msg='{0} is not exist or not a image file (jpg|jpeg|png).'.format(filename)
	    raise argparse.ArgumentTypeError(msg)
    return filename

def get_char(r, b, g,alpha=256): 
    if alpha == 0:  
        return ' '
    ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")
    length = len(ascii_char)  
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length  
    return ascii_char[int(gray/unit)]  
  
if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='convert a color image to strings image',prog='image2string')  
    parser.add_argument('-f','--file',required=True,type=isImage,help='source image file path,allow jpg|jpeg|png')     # 输入文件  
    parser.add_argument('-o','--output',default='output.txt',help='the output file path')   # 输出文件 
    args = parser.parse_args()
    infile = args.file  
    output = args.output  
    img = Image.open(infile)
    w,h=img.size
    if h>100:
	w = int((100/h)*w)
	h = int(100 / 2)
    im = img.resize((w,h),Image.NEAREST)  
    txt = ""  
    for i in range(h):  
	for j in range(w):
	    txt += get_char(*im.getpixel((j, i)))  
	txt += '\n'
    print(txt)
    # 字符画输出到文件
    with open(output,'w') as fp:
	fp.write(txt)
