package util

import (
	"bufio"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"
)

// DownLoadPath 下载文件路径
var DownLoadPath string

// InitDownLoad 初始化下载路径
func InitDownLoad(subpath string) {
	path, _ := os.Getwd()
	DownLoadPath = fmt.Sprintf("%s/%s/%s/", path, "mp3", subpath)
	if _, err := os.Stat(DownLoadPath); os.IsNotExist(err) {
		Logger.Printf("[%s] %s not exists", "info", DownLoadPath)
		os.MkdirAll(DownLoadPath, 0644)
	}
}

// DownLoadOne 真实下载单个文件
func DownLoadOne(link string, i int) error {
	index := strings.LastIndex(link, "/") + 1
	fileName := link[index:]
	fullName := DownLoadPath + fileName
	Logger.Printf("[%s] gorounting-%d 开始下载 %s", "info", i, fileName)

	uri, _ := url.Parse(link)
	client := &http.Client{
		Timeout: time.Duration(time.Minute * 10),
	}

	req, err := http.NewRequest("GET", link, nil)
	req.Header.Add("Host", uri.Host)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	response, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("从 %s 读取数据失败,err:%v", link, err)
	}

	if status := response.StatusCode; status != 200 {
		return fmt.Errorf("从 %s 读取数据失败,status_code:%d", link, status)
	}

	defer response.Body.Close()

	buffer := make([]byte, 4096)
	reader := bufio.NewReader(response.Body)
	fp, err := os.OpenFile(fullName, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0666)
	if err != nil {
		return fmt.Errorf("打开欲下载文件 %s 失败,err:%v", fullName, err)
	}

	defer fp.Close()
	writer := bufio.NewWriter(fp)
	for {
		n, err := reader.Read(buffer)
		if err == io.EOF {
			break
		}
		writer.Write(buffer[:n])
	}
	Logger.Printf("[%s] gorounting-%d 下载 %s 完成", "info", i, fileName)
	return nil
}

// DownLoad 从chan读取连接并完成文件下载
func DownLoad(sw *sync.WaitGroup, i int) error {
	for url := range DownChan {
		err := DownLoadOne(url, i)
		if err != nil {
			Logger.Printf("[%s] gorounting-%d 下载 %s 失败,err:%v", "error", i, url, err)
		}
	}
	sw.Done()
	return nil
}
