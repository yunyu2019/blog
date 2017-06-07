#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-11 11:00:08
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : 更新系统时间
import os
import re
import logging
import subprocess

logger=logging.getLogger('clock')
formatter=logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(message)s')
logger.setLevel(logging.INFO)
root='{app}/clock.log'.format(app=os.path.dirname(os.path.realpath(__file__)))
handler=logging.FileHandler(root,mode='a',encoding='utf-8')
handler.setFormatter(formatter)
logger.addHandler(handler)
ntp_server='cn.pool.ntp.org'
servers=['{0}.{1}'.format(x,ntp_server) for x in range(0,4)]
servers.append(ntp_server)
rule=re.compile('(\d+)% packet loss, time (\d+)ms',re.S)
rule1=re.compile('(\d+[\d\.]+\d+).* bytes of data',re.S)
ips=list()
logger.info('begin ping server')
for url in servers:
    cmd='ping -c {0} -w {1} {2}'.format(5,3,url)
    p=subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
    #out=p.stdout.read()
    out,err=p.communicate(timeout=15) #python3 支持的timeout参数
    if err:
       p.kill()
       continue
    else: 
       m=re.findall(rule,str(out))
       if len(m)>0 and m[0][0]=='0':
          m1=re.findall(rule1,str(out))
          ips.append(m1[0])
       else:
          continue

logger.info('ping over,get {0} ip,they are {1}'.format(len(ips),','.join(ips)))
if len(ips)<1:
   logger.info('can\'t update the time')
for ip in ips:
   cmd='ntpdate {0}'.format(ip)
   logger.info(cmd)
   p=subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
   out,err=p.communicate(timeout=15)  #python3 支持的timeout参数
   if err:
       p.kill()
       msg='{0} error {1}'.format(ip,str(err))
       logger.info(msg)
       continue
   else:
       logger.info(str(out))
       break
