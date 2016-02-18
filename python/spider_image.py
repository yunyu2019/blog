# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import urllib2
import time
import re
from threading import Thread
from Queue import Queue

THREAD_COUNT = 5

class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
 
    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()
 
class ThreadPool:
    """Pool of threads consuming tasks from a queue"""
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)
 
    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))
 
    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()

class Curlimg(object):
    def __init__(self,urls,dpath):
        self.urls=urls
        self.dpath=dpath
        self.mkdir(dpath)
    
    def save_img(self,subdir,img_url):
        fn=img_url.split('/')
        abpath=self.dpath+'\\'+subdir
        self.mkdir(abpath)
        try:
            data=urllib2.urlopen(img_url,timeout=20).read()
            f=open(abpath+'\\'+fn[-1],'wb')
            f.write(data)
            f.close()
            print 'save image ===========  ok'
        except:
            print 'save image error ==== OK'
            f=open(abpath+'\\err.txt','w')
            f.write(img_url)
            f.close()
    
    def mkdir(self,fdir):
        if not os.path.exists(fdir):
           os.makedirs(fdir)
          
    
    def imglist(self,page):
        params=str((page-1)*50)
        list_url=self.urls+'&pn='+params
        header={
            'Host':'tieba.baidu.com',
            'Cookie':'BAIDUID=6FCD0DBD41F73B9C3B52F704962FE2B5:FG=1; PSTM=1452238196; BIDUPSID=2C01F23219956D62164724AF3898473D; TIEBA_USERTYPE=1930a1e0f0b0147f3058ccc1; TIEBAUID=cb23caae2f82cf19384a575b; bdshare_firstime=1453185340057; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1453185341,1453440123,1453707944,1453708308; BDUSS=BNU1p0UWdkemtLbFhoa3dUbGgyenF0LXVJMkFqeFA0MFhTOVVNbnNTckdyYzlXQVFBQUFBJCQAAAAAAAAAAAEAAAA7kcUUempsODk1Mzc2ODk2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMYgqFbGIKhWNT; LONGID=348492091; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1457_17712_18284_18879_17945_18205_18964_18777_17001_17073_15265_12212_18090_18018',
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0'
        }
        req=urllib2.Request(list_url,headers=header)
        html=urllib2.urlopen(req).read()
        data=re.findall(r'<a class="thumbnail vpic_wrap"><img\b.* bpic="(.*?)"[^>]* />',html)
        print u"""开始抓取第 %d 页数据
共计 %d 张图片""" % (page,len(data))
        pool = ThreadPool(THREAD_COUNT)
        if data:
            for i in data:
                pool.add_task(self.save_img,str(page),i)
                time.sleep(1)
            pool.wait_completion()

if __name__ == '__main__':
    dpath='e:\\tieba'
    urls='http://tieba.baidu.com/f?kw=%E8%BD%AF%E5%A6%B9&ie=utf-8'
    for i in range(1,3):
        img=Curlimg(urls,dpath)
        img.imglist(i)
        
        
        
        