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
	flag.StringVar(&url, "link", "", "初始下载链接地址")
	flag.StringVar(&path, "path", "", "下载文件夹")
	flag.IntVar(&num, "num", 5, "并发下载文件数量")
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
		rand.Seed(time.Now().UnixNano())
		for url := range util.NextChan {
			cont, err := util.GetHTML(url)
			if err != nil {
				util.Logger.Printf("[%s] 从%s 获取url失败,err:%v", "error", url, err)
				continue
			}
			util.GetURL(url, cont)
			time.Sleep(time.Millisecond * time.Duration(rand.Intn(750)+1000)) //防止请求的过快，休眠750ms ~ 1750ms
		}
	}()

	for i := 0; i <= num; i++ {
		sw.Add(1)
		go util.DownLoad(&sw, i)
	}
	sw.Wait()
	util.Logger.Println("下载完成")
}
