package util

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"regexp"
	"strconv"
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
	indexRe  *regexp.Regexp
	metaRe   *regexp.Regexp
	timeout  time.Duration
)

func init() {
	downRe = regexp.MustCompile(`<iframe.*?src="(.*?)"`)
	nextRe = regexp.MustCompile(`<a.*?href='(.*?#down)'.*?>`)
	indexRe = regexp.MustCompile(`(\d+)-(\d+)`)
	metaRe = regexp.MustCompile(`<meta.*?charset=(\w+)>?`)
	NextChan = make(chan string, 100)
	DownChan = make(chan string, 100)
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
		return "", fmt.Errorf("抓取页面 %s 失败,err:%v", link, err)
	}
	defer response.Body.Close()
	html, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return "", fmt.Errorf("读取页面 %s 数据失败,err:%v", link, err)
	}

	charset := "gb2312"
	/*
	   if charset := getCharset(string(html)); charset != "" && charset != "utf-8" {
	       cont, err := transferUTF8(string(html), charset)
	       return cont, err
	   }
	   return string(html), nil
	*/
	cont, err := transferUTF8(string(html), charset)
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
		return "", fmt.Errorf("%s 转换成 utf-8 字符失败,err:%v", originCharset, err)
	}

	return s, nil
}

func getIndex(link string) int64 {
	temp := indexRe.FindAllStringSubmatch(link, -1)
	index, _ := strconv.ParseInt(temp[0][2], 10, 0)
	return index
}

func getCharset(html string) string {
	temp := metaRe.FindAllStringSubmatch(html, -1)
	if len(temp) > 0 {
		return temp[0][1]
	}
	return ""
}

// GetURL 从html内容获取下一集地址及当前下载链接地址
func GetURL(link, str string) {
	down := downRe.FindAllStringSubmatch(str, -1)
	next := nextRe.FindAllStringSubmatch(str, -1)
	if (len(down) < 1) && (len(next) < 1) {
		close(NextChan)
		close(DownChan)
		Logger.Printf("[%s] 从%s 获取url失败,出现了异常情况,close next url chan,close down chan", "error", link)
		return
	}

	if len(down) > 0 {
		origin := down[0][1]
		uri, _ := url.Parse(origin)
		if s := uri.Query().Get("url"); s != "" {
			DownChan <- s
			Logger.Printf("[%s] %s 加入下载队列", "info", s)
		}
	}

	currIndex := getIndex(link)
	if len(next) > 0 {
		nextIndex := getIndex(next[0][1])
		if (len(next) <= 1) && (nextIndex < currIndex) {
			close(NextChan)
			close(DownChan)
			Logger.Printf("[%s] close next url chan,close down chan", "info")
		} else {
			if s := next[0][1]; s != "" {
				NextChan <- s
				Logger.Printf("[%s] %s 加入url请求队列", "info", s)
			}
		}
	}
}
