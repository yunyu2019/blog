package main

import (
	"flag"
	"fmt"
	"math/rand"
	"spider/util"
	"sync"
	"time"
)

var sw sync.WaitGroup

func main() {
	var url string
	var path string
	var num int
	var one string
	flag.StringVar(&url, "link", "", "初始下载链接地址")
	flag.StringVar(&path, "path", "", "下载文件夹")
	flag.IntVar(&num, "num", 2, "并发下载文件数量")
	flag.StringVar(&one, "one", "", "下载单个文件")
	flag.Parse()

	if path == "" {
		fmt.Printf("path:%s 未指定\n", path)
		return
	}

	//初始化日志
	util.InitLog()
	//初始化下载目录
	util.InitDownLoad(path)

	if one != "" {
		err := util.DownLoadOne(one, 1)
		if err != nil {
			util.Logger.Panicf("下载 %s 失败,err:%v", one, err)
		}
		return
	}

	if url == "" {
		fmt.Printf("link:%s 未指定\n", url)
		return
	}

	cont, err := util.GetHTML(url)
	if err != nil {
		util.Logger.Panicf("[%s] 初始化下载 %s 失败,err:%v", "error", url, err)
	}

	util.GetURL(url, cont)

	go func() {
		rand.Seed(time.Now().UnixNano())
		for url := range util.NextChan {
			cont, err := util.GetHTML(url)
			if err != nil {
				util.Logger.Printf("[%s] 从%s 获取url失败,err:%v", "error", url, err)
				continue
			}
			util.GetURL(url, cont)
			time.Sleep(time.Millisecond * time.Duration(rand.Intn(1500)+1500)) //防止请求的过快，休眠1500ms ~ 3000ms
		}
	}()

	rand.Seed(time.Now().UnixNano())
	for i := 0; i <= num; i++ {
		sw.Add(1)
		go util.DownLoad(&sw, i)
		time.Sleep(time.Millisecond * time.Duration(rand.Intn(1500)+1500)) //防止请求的过快，休眠
	}
	sw.Wait()
	util.Logger.Println("下载完成")
}
