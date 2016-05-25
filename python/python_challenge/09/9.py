#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/good.html
import Image
import ImageDraw
from pc9data import first as body,second as head

color={
    'grass':(0x67,0xA6,0x45),
    'body':(0xBE,0xC0,0xBB),
    'head':(0x9C,0x4D,0x23)
}

canvas=Image.new('RGB',(480,480),color['grass'])
draw=ImageDraw.Draw(canvas)
draw.line(body)
draw.line(head)
"""
draw.line(zip(body[0::2],body[1::2]))
draw.line(zip(head[0::2],head[1::2]))
"""
canvas.save('9.png')

