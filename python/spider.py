# coding: UTF-8
import os
import time
import shutil
from threading import Thread
from Queue import Queue

THREAD_COUNT = 5
file_list=[]

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

def copyer(file,spath,dpath):
	absf=spath+file
	abdf=dpath+file
	nums=0
	if not os.path.exists(abdf):
	    nums=len(abdf.split('\\'))
        if nums > 3:
            flag=abdf.rindex('\\')
            subdir=abdf[0:flag]
            if not os.path.exists(subdir):
            	os.makedirs(subdir)
            print u'正在复制 %s' % absf
            shutil.copy(absf,abdf)
        else:
            print u'%s 已经复制过了' %  absf
def listdir(spath):
    for fp in os.listdir(spath):
    	absp=os.path.join(spath,fp)
    	if os.path.isfile(absp):
    	   file_list.append(absp[5:])
    	elif os.path.isdir(absp):
    		listdir(absp)
    return file_list		
if __name__ == '__main__':
    spath=u'd:\软件'
    dpath='e:\software'
    pool = ThreadPool(5)
    files=listdir(spath)
    if not os.path.exists(dpath):
        os.makedirs(dpath)
    for file in files:
    	pool.add_task(copyer,file,spath,dpath)
    	time.sleep(1)
    pool.wait_completion()
