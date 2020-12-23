package util

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"strings"
	"time"

	"golang.org/x/net/html/charset"
	"golang.org/x/text/transform"
)

var (
	// NextChan 请求下一集链接通道
	NextChan chan string
	// DownChan 下载链接通道
	DownChan chan string
	downRe   *regexp.Regexp
	nextRe   *regexp.Regexp
	timeout  time.Duration
)

func init() {
	downRe = regexp.MustCompile(`<iframe.*?src="(.*?)"`)
	nextRe = regexp.MustCompile(`<a.*?href='(.*?#down)'.*?>`)
	NextChan = make(chan string, 10)
	DownChan = make(chan string, 10)
	timeout = time.Duration(time.Second * 10)
}

// GetHTML 获取url地址内容
func GetHTML(link string) (string, error) {
	uri, _ := url.Parse(link)
	client := &http.Client{
		Timeout: timeout,
	}

	req, err := http.NewRequest("GET", link, nil)
	req.Header.Add("Host", uri.Host)
	req.Header.Add("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
	response, err := client.Do(req)
	if err != nil {
		fmt.Printf("抓取页面 %s 失败,err:%v\n", link, err)
		return "", err
	}
	defer response.Body.Close()
	html, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Printf("读取页面 %s 数据失败,err:%v\n", link, err)
		return "", err
	}

	cont, err := transferUTF8(string(html), "gb2312")
	return cont, err
}

func transformString(t transform.Transformer, s string) (string, error) {
	r := transform.NewReader(strings.NewReader(s), t)
	b, err := ioutil.ReadAll(r)
	return string(b), err
}

func transferUTF8(source, originCharset string) (string, error) {
	e, _ := charset.Lookup(originCharset)
	s, err := transformString(e.NewDecoder(), source)
	if err != nil {
		fmt.Printf("%s 转换成 utf-8 字符失败,err:%v\n", originCharset, err)
	}
	return s, nil
}

// GetURL 从html内容获取下一集地址及当前下载链接地址
func GetURL(str string) {
	next := nextRe.FindAllStringSubmatch(str, -1)
	if len(next) > 0 {
		if len(next[0]) <= 1 {
			close(NextChan)
		} else {
			if s := next[0][1]; s != "" {
				fmt.Printf("%s 加入url请求队列\n", s)
				NextChan <- s
			}
		}
	}

	down := downRe.FindAllStringSubmatch(str, -1)
	if len(down) > 0 {
		origin := down[0][1]
		uri, _ := url.Parse(origin)
		if s := uri.Query().Get("url"); s != "" {
			fmt.Printf("%s 加入下载队列\n", s)
			DownChan <- s
		}
	}
}
