#!/usr/bin/python
# -*- coding: utf-8 -*-
# note:
#www.pythonchallenge.com/pc/return/uzi.html
import datetime
years=[]
for year in range(1996,1582,-20):
    wkday=datetime.date(year,1,1).weekday()
    if wkday==3:
        years.append(year)
print years
"""
得到1756-01-27,莫扎特(mozart)的生日
"""