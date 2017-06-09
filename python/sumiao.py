#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-05 17:39:42
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : 将图片转换成灰度图片
"""
#run in python3 env
pip3 install pillow
pip3 install numpy
"""

import os
import time
import argparse
import numpy as np
from PIL import Image

def isImage(filename):
    allows=('.jpg','.jpeg','.png')
    if  not filename.endswith(allows) or not os.path.isfile(filename):
        msg='{0} is not exist or not a image file (jpg|jpeg|png).'.format(filename)
        raise argparse.ArgumentTypeError(msg)
    return filename

def conver2gray(sta,end,depths=10):
    a = np.asarray(Image.open(sta).convert('L')).astype('float')
    depth = depths
    grad = np.gradient(a)  # 取图像灰度的梯度值
    grad_x, grad_y = grad  # 分别取横纵图像梯度值
    grad_x = grad_x * depth / 100.
    grad_y = grad_y * depth / 100.
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A
    vec_el = np.pi / 2.2  # 光源的俯视角度，弧度值
    vec_az = np.pi / 4.  # 光源的方位角度，弧度值
    dx = np.cos(vec_el) * np.cos(vec_az)  # 光源对x 轴的影响
    dy = np.cos(vec_el) * np.sin(vec_az)  # 光源对y 轴的影响
    dz = np.sin(vec_el)  # 光源对z 轴的影响
    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  # 光源归一化
    b = b.clip(0, 255)
    im = Image.fromarray(b.astype('uint8'))  # 重构图像
    im.save(end)

def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(description='convert a color image to gray image',prog='image2gray')
    parser.add_argument('-f','--file',required=True,type=isImage,help='source image file path,allow jpg|jpeg|png')
    parser.add_argument('-g','--gray',default=10,type=int,help='the value of gray,the larger the value, the deeper the color')
    parser.add_argument('-o','--output',required=True,help='the output image file path')
    args = parser.parse_args()
    source = args.file
    gray = args.gray
    dist=args.output
    conver2gray(sta=source,end=dist,depths=gray)
    end_time = time.time()
    exect_time=round(end_time - start_time,3)
    print('程序运行了{0}s'.format(exect_time))

if __name__ == '__main__':
    main()
    
