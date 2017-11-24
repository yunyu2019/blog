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
    logger=None

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
           out=out.decode('utf-8')
           err=err.decode('utf-8')
        except TimeoutExpired:
           p.kill()
           _,err=p.communicate()
           out=False
           err=err.decode('utf-8')
        finally:
           return out,err

    def pings(self):
        rule=re.compile('(\d+)% packet loss, time (\d+)ms',re.S)
        rule1=re.compile('(\d+[\d\.]+\d+).* bytes of data',re.S)
        for url in self.servers:
           cmd='ping -c {0} -W {1} -q {2}'.format(5,3,url)
           out,err=self.shellCmd(cmd)
           if not out:
               self.logger.info('ping {0} error,{1}'.format(url,err))
               continue

           m=re.findall(rule,str(out))
           if len(m)>0 and m[0][0]=='0':
              m1=re.findall(rule1,str(out))
              if len(m1)>0:
                 self.logger.info('get {} from {}'.format(m1[0],url))
                 yield m1[0]

    def ntpdates(self,ip):
        cmd='/usr/sbin/ntpdate {0}'.format(ip) #默认执行的是/bin/sh下的命令，但ntpdate命令不在该目录下
        self.logger.info(cmd)
        out,err=self.shellCmd(cmd)
        if out:
            self.logger.info(out.strip())
            return True

        msg='{0} error {1}'.format(ip,err)
        self.logger.info(msg)
        return False

    def run(self):
        self.logger.info('begin ping server')
        for ip in self.pings():
            flag=self.ntpdates(ip)
            if flag:
               break

        self.logger.info('ntpdate time over')

ntp=ntpdateOs()
ntp.run()