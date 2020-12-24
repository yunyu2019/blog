package util

import (
	"fmt"
	"log"
	"os"
	"time"
)

var (
	// Logger 日志句柄
	Logger *log.Logger
)

// InitLog 初始化日志
func InitLog() {
	path, _ := os.Getwd()

	fullPath := path + "/log/"
	if _, err := os.Stat(fullPath); os.IsNotExist(err) {
		os.MkdirAll(fullPath, 0644)
	}

	logName := fmt.Sprintf("%s/%s_%s.log", fullPath, "log", time.Now().Format("2006-01-02"))
	logFile, err := os.OpenFile(logName, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalln("打开日志文件失败：", err)
	}

	Logger = log.New(logFile, "", log.Ldate|log.Lmicroseconds)
}
