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

	util.InitDownLoad(path)

	cont, err := util.GetHTML(url)
	if err != nil {
		panic(err)
	}
	util.GetURL(cont)

	go func() {
		for url := range util.NextChan {
			cont, err := util.GetHTML(url)
			if err != nil {
				fmt.Printf("从%s 获取url失败,err:%v\n", url, err)
				continue
			}
			util.GetURL(cont)
		}
	}()

	for i := 0; i <= 5; i++ {
		sw.Add(1)
		go util.DownLoad(&sw, i)
	}
	sw.Wait()
}
