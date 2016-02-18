#!/usr/bin/python
#-*-coding:UTF-8-*-
import os
import urllib2
import urlparse
import time
import re
import codecs
from threading import Thread
from Queue import Queue
import MySQLdb
from pypinyin import lazy_pinyin

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

class Tool:
    #去除img标签,1-7位空格,&nbsp;
    removeImg = re.compile('<img.*?>| {1,7}|&nbsp;|&middot;|[-|.]{3,}')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    #将多行空行删除
    removeNoneLine = re.compile('\n+')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        x = re.sub(self.removeNoneLine,"\n",x)
        #strip()将前后多余内容删除
        return x.strip()

"""
#用户表
CREATE TABLE `user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT 'mm姓名',
  `age` smallint(3) unsigned DEFAULT '0' COMMENT '年龄',
  `profile_url` varchar(50) DEFAULT NULL COMMENT '个人主页地址',
  `faceimg` varchar(100) DEFAULT NULL COMMENT '个人头像',
  `tags` varchar(50) DEFAULT NULL COMMENT '个人标签',
  `descp` varchar(500) DEFAULT NULL COMMENT '个人简介',
  `city` varchar(20) DEFAULT NULL COMMENT '来自城市',
  `imgnums` smallint(10) unsigned DEFAULT '0' COMMENT '导购 图片总数',
  `integral` int(10) unsigned DEFAULT '0' COMMENT '总积分',
  `fans` int(10) unsigned DEFAULT '0' COMMENT '粉丝数量',
  `signnum` int(10) unsigned DEFAULT '0' COMMENT '签约数量',
  `rates` varchar(20) DEFAULT '0.00' COMMENT '好评率',
  `model_img` varchar(100) DEFAULT NULL COMMENT '生活时尚图秀',
  `big_img` varchar(200) DEFAULT NULL COMMENT '大图头像',
  `life_img` varchar(200) DEFAULT NULL COMMENT '大幅生活照',
  `pinyin` varchar(20) DEFAULT NULL COMMENT '拼音名字',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

#个人资料表
CREATE TABLE `profile` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '关联的用户id',
  `nicename` varchar(50) DEFAULT NULL COMMENT '昵称',
  `borthday` varchar(50) DEFAULT NULL COMMENT '生日',
  `blood` varchar(20) DEFAULT NULL COMMENT '血型',
  `school` varchar(50) DEFAULT NULL COMMENT '毕业院校',
  `style` varchar(30) DEFAULT NULL COMMENT '风格',
  `height` varchar(20) DEFAULT NULL COMMENT '身高',
  `weight` varchar(20) DEFAULT NULL COMMENT '体重',
  `solid` varchar(20) DEFAULT NULL COMMENT '三维',
  `bar` varchar(50) DEFAULT NULL COMMENT '胸型',
  `shoes` varchar(10) DEFAULT NULL COMMENT '鞋码',
  `exprince` text COMMENT '个人经历',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
"""

class Taobao(object):
    """抓取淘宝mm的程序"""
    def __init__(self,urls,dpath,starts,ends):
        self.urls=urls
        self.dpath=dpath
        self.starts=starts
        self.ends=ends
        self.tool =Tool()
    
    def mkdir(self,fdir):
        if not os.path.exists(fdir):
           os.makedirs(fdir)
    
    def gettime(self):
        curr_time=time.localtime()
        curr_time=time.strftime('%Y-%m-%d %H:%M:%S',curr_time)
        return curr_time
           
    def bra(self,s):
        rule=re.compile('[6-9]{1}[0-9]{1}[a-g|A-G]?',re.I)
        flag=re.match(rule,s)
        if flag:
            m=re.search('(\d+)(\w?)',s)
            num=m.group(1)
            num=int(num)
            bar=30
            if num>=68 and num<=72:
                bar=32
            elif num>=73 and num<=77:
                bar=34
            elif num>=78 and num<=82:
                bar=36
            elif num>=83 and num<=87:
                bar=38
            elif num>=88 and num<=92:
                bar=40
            upbar=m.group(2)
            if upbar!='':
                bar=str(bar)+upbar.upper()
            return bar
        else:
            return s
        
    def getContent(self,page):
        """获取页面的内容信息"""
        params=str(page)
        list_url=self.urls+'?page='+params
        header={
            'Host':'mm.taobao.com',
            'Cookie':'thw=cn; miid=7592320213040609111; cna=1u4ZD8yNDC8CAcpqqeiyKnT0; isg=0830773A8D1358D2A801D5B0D3BFE2E2; uc3=nk2=txBJoUSGvqg%3D&id2=UU23C%2B9%2BZQMNjA%3D%3D&vt3=F8dASccesVq5kGzOoP4%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu4E91%5Cu8BED2019; tracknick=%5Cu4E91%5Cu8BED2019; _cc_=VT5L2FSpdA%3D%3D; tg=0; mt=ci=0_1; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; CNZZDATA30063598=cnzz_eid%3D55660832-1454057992-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454057992; CNZZDATA30064598=cnzz_eid%3D620701788-1454056446-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454056661; CNZZDATA30063600=cnzz_eid%3D880614795-1454056379-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454060018; l=Aj09zKxfGs7gtZD/TZQ/7wWezZM3s3Ej; v=0; _tb_token_=DlV8upUHUziAwx3; JSESSIONID=1C6390961BDC114F40264472BEDFF54C; uc1=cookie14=UoWyiqrPiMUB%2Fw%3D%3D; cookie2=1cf6800e7b26483ec5ccc10658927160; t=cf614df5632b038d72bf347e2a24d6b3',
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0'
        }
        try:
            req=urllib2.Request(list_url,headers=header)
            html=urllib2.urlopen(req,data=None,timeout=10).read().decode('gbk')
            rule=re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>.*?<em>(.*?)</em>.*?<em><strong>(.*?)</strong>.*?</em>.*?<img data-ks-lazyload="(.*?)".*?/>.*?class="popularity".*?<dd>.*?(\d+).*?</dd>.*?class="info-detail".*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<li>.*?<strong>(.*?)</strong>.*?</li>.*?<p class="description">(.*?)</p>?',re.S)
            content=re.findall(rule,html)
            return content
        except urllib2.HTTPError,e:
            print u'获取数据失败'
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            curr_time=self.gettime()
            fp=codecs.open(self.dpath+'/error.log','a','utf-8')
            fp.write(curr_time+u' 获取第'+params+u'页数据失败，原因:'+errors+'\n')
            fp.close()
            content=()
            return content
        except urllib2.URLError,e:
            print u'链接地址不正确'
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            curr_time=self.gettime()
            fp=codecs.open(self.dpath+'/error.log','a','utf-8')
            fp.write(curr_time+u' 获取第'+params+u'页数据失败，原因:'+errors+'\n')
            fp.close()
            content=()
            return content
        else:
            pass
        
    def saveimg(self,imgurl,subdir,descp):
        """保存图片"""
        img_url='https:'+imgurl
        fn=img_url.split('/')
        abpath=self.dpath+'/'+subdir
        self.mkdir(abpath)
        try:
            data=urllib2.urlopen(img_url,timeout=20).read()
            f=open(abpath+'/'+fn[-1],'wb')
            f.write(data)
            f.close()
            print u'save %s image ===========  ok' % descp
        except urllib2.HTTPError,e:
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            print u'save image error ==== OK' % descp
            curr_time=self.gettime()
            f=codecs.open(abpath+'/error.log','a','utf-8')
            f.write(curr_time+u' 保存图片:'+img_url+u'失败,原因:'+errors+'\n')
            f.close()
        except urllib2.URLError,e:
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            curr_time=self.gettime()
            fp=codecs.open(abpath+'/error.log','a','utf-8')
            f.write(curr_time+u' 保存图片:'+img_url+u'失败,原因:'+errors+'\n')
            fp.close()
        else:
            pass
    
    def getProfile(self,prourl,page):
        """获取mm个人资料"""
        prourl='https:'+prourl
        result=urlparse.urlparse(prourl)
        params=urlparse.parse_qs(result.query)
        user_id=params['user_id'][0]
        profile_url='https://mm.taobao.com/self/info/model_info_show.htm?user_id='+user_id
        header={
            'Host':'mm.taobao.com',
            'cookie':'swfstore=294769; thw=cn; miid=7592320213040609111; cna=1u4ZD8yNDC8CAcpqqeiyKnT0; isg=0830773A8D1358D2A801D5B0D3BFE2E2; uc3=nk2=txBJoUSGvqg%3D&id2=UU23C%2B9%2BZQMNjA%3D%3D&vt3=F8dASccesVq5kGzOoP4%3D&lg2=URm48syIIVrSKA%3D%3D; lgc=%5Cu4E91%5Cu8BED2019; tracknick=%5Cu4E91%5Cu8BED2019; _cc_=VT5L2FSpdA%3D%3D; tg=0; mt=ci=0_1; CNZZDATA30063598=cnzz_eid%3D55660832-1454057992-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454294534; v=0; _tb_token_=te7941FAFzKUtf7; CNZZDATA30064598=cnzz_eid%3D620701788-1454056446-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454376870; CNZZDATA30063600=cnzz_eid%3D880614795-1454056379-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1454375141; l=Ah4ep2qW6duvGBPi2rFs4ZnD7r5g3-JZ; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; JSESSIONID=CBB46AA5B26B61A77FE3E8F34A9E8801; uc1=cookie14=UoWyiqv3bfJSJA%3D%3D; cookie2=15fca6d3c3578cb62acba0a81d2504fb; t=cf614df5632b038d72bf347e2a24d6b3',
            'User-Agent':'Mozilla/5.0 (Windows NT 5.1; rv:17.0) Gecko/20100101 Firefox/17.0'          
        }
        try:
            req=urllib2.Request(profile_url,headers=header)
            html=urllib2.urlopen(req,data=None,timeout=10).read().decode('gbk')
            rule=re.compile('<ul class="mm-p-info-cell clearfix".*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?><label.*?<span>(.*?)</span>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<li.*?>.*?<p>(.*?)</p>.*?<div class="mm-p-info mm-p-experience-info">.*?<p>(.*?)</p>.*?class="mm-p-modelCard".*?<img src="(.*?)".*?/>?',re.S)
            profile=re.findall(rule,html)
            return profile[0]
        except urllib2.HTTPError,e:
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            curr_time=self.gettime()
            fp=codecs.open(self.dpath+'/error.log','a','utf-8')
            fp.write(curr_time+' '+str(page)+u'页 用户'+user_id+u'错误'+errors+'\n')
            fp.close()
        except urllib2.URLError,e:
            errors=''
            if hasattr(e,'reason'):
                errors=str(e.reason)
            elif hasattr(e,'code'):
                errors='error code:'+e.code+' message:'+e.reade()
            curr_time=self.gettime()
            fp=codecs.open(self.dpath+'/error.log','a','utf-8')
            fp.write(curr_time+' '+str(page)+u'页 用户'+user_id+u'错误'+errors+'\n')
            fp.close()
        else:
            pass
        
    def saveAll(self,contents,page):
        sname=contents[3]
        profiles=self.getProfile(contents[2],page)
        if sname=='':
            sname=profiles[0]
        user=lazy_pinyin(sname)
        username=''
        for uls in user:
            username+=uls
        abpath=self.dpath+'/'+str(page)+'/'+username
        self.mkdir(abpath)
        conn=MySQLdb.connect(host="127.0.0.1",user="root",passwd="123456",db="taobao",charset="utf8")
        cursor = conn.cursor()
        print u'开始保存 %s 基本信息到user表' % sname
        descp=self.tool.replace(contents[13].encode('utf-8'))
        big_img=self.tool.replace(contents[8].encode('utf-8'))
        life_img=self.tool.replace(profiles[13].encode('utf-8'))
        try:
            sql="insert into `user` (`name`,`age`,`profile_url`,`faceimg`,`tags`,`descp`,`city`,`imgnums`,`integral`,`fans`,`signnum`,`rates`,`model_img`,`big_img`,`life_img`,`pinyin`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            n=cursor.execute(sql,(sname,contents[4],'https:'+contents[0],'https:'+contents[1],contents[6],contents[14],contents[5],contents[12],contents[9],contents[7],descp,contents[11],'','https:'+big_img,'https:'+life_img,username))
            print u'开始保存 %s 详细信息profile表' % sname
            userid=conn.insert_id()
            borthday=self.tool.replace(profiles[1])
            school=self.tool.replace(profiles[5])
            exprince=self.tool.replace(profiles[12])
            bar=self.bra(profiles[10])
            sql1="insert into `profile` (`user_id`,`nicename`,`borthday`,`blood`,`school`,`style`,`height`,`weight`,`solid`,`bar`,`shoes`,`exprince`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            n=cursor.execute(sql1,(str(userid),profiles[0],borthday,profiles[4],school,profiles[6],profiles[7],profiles[8],profiles[9],bar,profiles[11],exprince))
        except MySQLdb.Error,e:
            curr_time=gettime()
            fp=codecs.open(self.dpath+'/error.log','a','utf-8')
            fp.write(curr_time+' '+str(page)+u'页 '+sname+u'错误:'+str(e)+'\n')
            fp.close()
        print u'开始保存 %s 详细信息到文件' % sname
        fp=codecs.open(abpath+'/profile.txt','wb','utf-8')
        for v in contents:
            temp=v.replace('\t','')
            temp=v.replace('\n','')
            fp.write(temp+'\n')
        for j in profiles:
            temp=j.replace('\t','')
            temp=j.replace('\n','')
            fp.write(temp+'\n')
        fp.close()
        self.saveimg(contents[1],str(page)+'/'+username,sname+u'小图')
        self.saveimg(contents[8],str(page)+'/'+username,sname+u'大图')
        self.saveimg(profiles[13],str(page)+'/'+username,sname+u'生活图')
        print u"""%s信息 保存完毕
        """ % sname
    
    def run(self):
        pool = ThreadPool(THREAD_COUNT)
        for i in range(self.starts,self.ends):
            print u'开始抓取第 %d 页数据' % i
            content=self.getContent(i)
            num=len(content)
            curr_time=self.gettime()
            fp=codecs.open(self.dpath+'/splider.log','a','utf-8')
            fp.write(curr_time+u' 开始抓取第 '+str(i)+u' 页数据 共计 '+str(num)+u' 条记录\n')
            fp.close()
            for cont in content:
                pool.add_task(self.saveAll,cont,i)
                time.sleep(1)
            pool.wait_completion()
    
if __name__ == '__main__':
    mm=Taobao('https://mm.taobao.com/json/request_top_list.htm','e:/taobao',761,801)
    mm.run()
    
    
        
        
        
