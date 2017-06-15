#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-05-11 11:00:08
# @Author  : Yunyu2019 (yunyu2010@yeah.net)
# @Link    : ${link}
# @descp   : ntpdate the os system time
import os
import re
import logging
import subprocess

class ntpdateOs(object):
    """ntpdate the os system time"""
    servers=list()
    logger=False
    ips=list()

    def __init__(self):
        self.initServers()
        self.initLogs()

    def initServers(self):
        ntp_server='cn.pool.ntp.org'
        servers=['{0}.{1}'.format(x,ntp_server) for x in range(0,4)]
        servers.append(ntp_server)
        self.servers=servers

    def initLogs(self):
        logger=logging.getLogger('clock')
        formatter=logging.Formatter('%(asctime)s  %(message)s')
        logger.setLevel(logging.INFO)
        root='{app}/clock.log'.format(app=os.path.dirname(os.path.realpath(__file__)))
        handler=logging.FileHandler(root,mode='a',encoding='utf-8')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger=logger

    def shellCmd(self,cmd,timeout=15):
        p=subprocess.Popen(cmd,stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell = True)
        try:
           out,err=p.communicate(timeout=timeout)  #python3.3开始支持timeout参数
           return out,err
        except TimeoutExpired:
           p.kill()
           out,err=p.communicate()
           return False,err

    def pings(self):
        self.logger.info('begin ping server')
        rule=re.compile('(\d+)% packet loss, time (\d+)ms',re.S)
        rule1=re.compile('(\d+[\d\.]+\d+).* bytes of data',re.S)
        for url in self.servers:
           cmd='ping -c {0} -w {1} {2}'.format(5,3,url)
           out,err=self.shellCmd(cmd)
           if out:
               m=re.findall(rule,str(out))
               if len(m)>0 and m[0][0]=='0':
                  m1=re.findall(rule1,str(out))
                  if len(m1)>0:
                     self.ips.append(m1[0])
                  else:
                     continue
               else:
                  continue
           else:
               self.logger.info('ping {0} error,{1}'.format(url,err.decode('utf-8')))
               continue

        self.logger.info('ping over,get {0} ip,they are {1}'.format(len(self.ips),','.join(self.ips)))

    def ntpdates(self):
        for ip in self.ips:
            cmd='/usr/sbin/ntpdate {0}'.format(ip) #默认执行的是/bin/sh下的命令，但ntpdate命令不在该目录下
            self.logger.info(cmd)
            out,err=self.shellCmd(cmd)
            if out:
                self.logger.info('success,{0}'.format(str(out)))
                break
            else:
                msg='{0} error {1}'.format(ip,err.decode('utf-8'))
                self.logger.info(msg)
                continue

        self.logger.info('ntpdate time over')

    def run(self):
        self.pings()
        if len(self.ips)<1:
           self.logger.info('can\'t update the system time')
           exit()

        self.ntpdates()

ntp=ntpdateOs()
ntp.run()