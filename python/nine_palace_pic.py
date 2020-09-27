#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 生成九宫格图片

import os
import argparse
from PIL import Image,ImageSequence,ImageFilter

def isImage(filename):
    allows=('.jpg','.jpeg','.png')
    if  not filename.endswith(allows) or not os.path.isfile(filename):
        msg='{0} is not exist or not a image file (jpg|jpeg|png).'.format(filename)
        raise argparse.ArgumentTypeError(msg)
    return filename

def run(img):
    x = 0
    y = 0
    index = 1
    base_name,ext = os.path.splitext(img)
    im = Image.open(img)
    width = im.size[0]//3
    height = im.size[1]//3
    for i in range(3):
        for j in range(3):
            filename = u'{name}_{index}{ext}'.format(name=base_name,index=index,ext=ext)
            print(filename)
            crop = im.crop((x, y, x + width, y + height))
            crop.save(filename)
            x += width
            index += 1

        x = 0
        y += height

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = '将图片转换成九宫格图片',prog = 'image2Nine')
    parser.add_argument('-i','--image',required = True,type = isImage,help = 'source image file path,allow jpg|jpeg|png')
    args = parser.parse_args()
    img = args.image
    run(img)