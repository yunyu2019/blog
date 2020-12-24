package main

import (
	"flag"
	"fmt"
	"spider/util"
	"sync"
)

var sw sync.WaitGroup

func main() {
	var url string
	var path string
	flag.StringVar(&url, "link", "", "初始下载链接地址")
	flag.StringVar(&path, "path", "", "下载文件夹")
	flag.Parse()

	if url == "" || path == "" {
		fmt.Printf("link:%s path:%s 未指定\n", url, path)
		return
	}

	//初始化日志
	util.InitLog()
	//初始化下载目录
	util.InitDownLoad(path)

	cont, err := util.GetHTML(url)
	if err != nil {
		util.Logger.Panicf("[%s] 初始化下载 %s 失败,err:%v", "error", url, err)
	}
	util.GetURL(url, cont)
	go func() {
		for url := range util.NextChan {
			cont, err := util.GetHTML(url)
			if err != nil {
				util.Logger.Printf("[%s] 从%s 获取url失败,err:%v", "error", url, err)
				continue
			}
			util.GetURL(url, cont)
		}
	}()

	for i := 0; i <= 5; i++ {
		sw.Add(1)
		go util.DownLoad(&sw, i)
	}
	sw.Wait()
}
