#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-05 17:39:42
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : 将图片转换成素描图片
"""
#run in python3 env
pip3 install pillow
pip3 install numpy
"""

import os
import time
from PIL import Image
import numpy as np

def image(sta,end,depths=10):
    a = np.asarray(Image.open(sta).convert('L')).astype('float')
    depth = depths  # (0-100)
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
    xss = input("请输入0-100的数值(数值越大，颜色越深,默认值10):")
    xs = int(xss) if xss else 10
    source=input('请输入原图路径:')
    if not os.path.isfile(source):
    	print('图片不存在')
    	exit()
    basename=os.path.basename(source)
    dist=source.replace(basename,'s_{0}'.format(basename))
    image(sta=source,end=dist,depths=xs)
    end_time = time.time()
    exect_time=round(end_time - start_time,3)
    print('程序运行了{0}s'.format(exect_time))

if __name__ == '__main__':
    main()
