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
		fmt.Printf("%s not exists\n", DownLoadPath)
		os.MkdirAll(DownLoadPath, 0644)
	}
}

// DownLoadOne 真实下载单个文件
func DownLoadOne(link string, i int) error {
	index := strings.LastIndex(link, "/") + 1
	fileName := link[index:]
	fullName := DownLoadPath + fileName
	fmt.Printf("gorounting-%d 开始下载 %s\n", i, fileName)

	uri, _ := url.Parse(link)
	client := &http.Client{
		Timeout: time.Duration(time.Minute * 10),
	}

	req, err := http.NewRequest("GET", link, nil)
	req.Header.Add("Host", uri.Host)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	response, err := client.Do(req)
	if err != nil {
		fmt.Printf("读取 %s 数据失败,err:%v\n", link, err)
		return err
	}

	if status := response.StatusCode; status != 200 {
		fmt.Printf("读取原始数据 %s 出问题了,status_code:%d\n", link, status)
		return fmt.Errorf("读取原始数据 %s 失败", link)
	}

	defer response.Body.Close()

	buffer := make([]byte, 4096)
	reader := bufio.NewReader(response.Body)
	fp, err := os.OpenFile(fullName, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println("打开结果文件失败")
		return err
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
	fmt.Printf("gorounting-%d 下载 %s 完成\n", i, fileName)

	return nil
}

// DownLoad 从chan读取连接并完成文件下载
func DownLoad(sw *sync.WaitGroup, i int) error {
	for {
		url, ok := <-DownChan
		if !ok {
			break
		}
		err := DownLoadOne(url, i)
		if err != nil {
			fmt.Printf("%s 下载文件失败,err:%v\n", url, err)
		}
	}
	sw.Done()
	return nil
}
