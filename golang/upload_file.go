/*
* 断点续传文件实验
 */
package main

import (
	"flag"
	"fmt"
	"io"
	"os"
	"path"
	"strconv"
)

//检测文件目录是不是存在
func CheckFile(s string) (flag bool, isdir bool, name string, size int64) {
	f, err := os.Stat(s)
	flag = true
	if os.IsNotExist(err) {
		flag = false
	}
	if f.IsDir() {
		isdir = true
	} else {
		name = f.Name()
		size = f.Size()
	}
	return flag, isdir, name, size
}

func upload(source string, dist string) bool {
	sflag, sisdir, sourceFile, size := CheckFile(source)
	if !sflag {
		fmt.Printf("源地址 %s 不存在\n", source)
		return false
	}
	if sisdir {
		fmt.Printf("源地址 %s 不是一个文件\n", source)
		return false
	}

	distFlag, disdir, _, _ := CheckFile(dist)
	if !distFlag {
		fmt.Printf("目标地址 %s 不存在\n", dist)
		return false
	}
	if !disdir {
		fmt.Printf("目标地址 %s 不是一个目录\n", dist)
		return false
	}

	var total int64
	distFile := path.Join(dist, sourceFile)
	tempFile := path.Join(dist, sourceFile+"_temp")
	fmt.Println(sourceFile)

	fTemp, err := os.OpenFile(tempFile, os.O_CREATE|os.O_RDWR, 0666)
	if os.IsNotExist(err) {

	} else {
		buf := make([]byte, 100)
		n1, _ := fTemp.Read(buf)
		fmt.Println(string(buf[:n1]))
		total, _ = strconv.ParseInt(string(buf[:n1]), 10, 64)
	}
	fmt.Printf("初始化total: %d \n", total)
	fs, err := os.OpenFile(source, os.O_RDONLY, 0666)
	if err != nil {
		fmt.Printf("源文件 %s 打开失败\n", source)
		return false
	}
	defer fs.Close()

	fd, err := os.OpenFile(distFile, os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Printf("目标文件 %s 打开失败\n", dist)
		return false
	}
	defer fd.Close()

	fs.Seek(total, io.SeekStart)
	fd.Seek(total, io.SeekStart)

	readBuf := make([]byte, 1024*32)
	finish := false
	for {
		n, err := fs.Read(readBuf)
		if n == 0 || err == io.EOF {
			finish = true
			break
		}
		wn, _ := fd.Write(readBuf[:n])
		total += int64(wn)
		fTemp.Seek(0, io.SeekStart)
		fTemp.WriteString(strconv.FormatInt(total, 10))
		fmt.Printf("当前上传进度 %.3f \n", float64(total)/float64(size)*float64(100))
		//time.Sleep(1 * time.Second)
	}
	fTemp.Close()

	if finish {
		os.Remove(tempFile)
	}

	return true
}

func main() {
	var source, dist string
	flag.StringVar(&source, "i", "", "源文件地址")
	flag.StringVar(&dist, "o", "", "目标地址目录")
	flag.Parse()
	flag := upload(source, dist)
	if flag {
		fmt.Println("已经传输完毕")
	} else {
		fmt.Println("传输意外终止")
	}
}
