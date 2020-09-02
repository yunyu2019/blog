package main

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"os"
	"strconv"
	"time"

	"pool/libary"
	"pool/model"

	"github.com/go-redis/redis/v7"
	"github.com/go-sql-driver/mysql"
)

var (
	jobLen  int = 8
	resLen  int = 5
	poolNum int = 4

	loggers   *log.Logger
	current   int64
	limit     string
	paperKey  string
	listKey   string
	startTime int64
	duration  int64
	statArr   []string
	data      []string
)

func init() {
	logName := fmt.Sprintf("%s-%s.log", "mock_answer_write_pool", time.Now().Format("2006-01-02"))
	logFile, err := os.OpenFile(logName, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalln("打开日志文件失败：", err)
	}

	loggers = log.New(logFile, "", log.Ldate|log.Lmicroseconds)
}

func main() {
	var listSize int = 100
	redisConfig := redis.Options{
		Addr:     "localhost:6379",
		Password: "",
		DB:       0,
	}

	client := redis.NewClient(&redisConfig)
	_, err := client.Ping().Result()
	if err != nil {
		loggers.Printf("[%s] redis服务不可用,%v\n", "info", err)
		return
	}

	mysqlParams := make(map[string]string)
	mysqlParams["charset"] = "utf8mb4"

	mysqlConfig := mysql.Config{
		User:                 "root",
		Passwd:               "",
		Net:                  "tcp",
		Addr:                 "127.0.0.1:3306",
		DBName:               "test",
		Timeout:              5 * time.Second,
		Collation:            "utf8mb4_unicode_ci",
		Params:               mysqlParams,
		AllowNativePasswords: true,
	}

	mysqlDsn := mysqlConfig.FormatDSN()

	db, err := sql.Open("mysql", mysqlDsn)
	if err != nil {
		loggers.Printf("[%s] dsn:%s open mysql error,%v\n", "error", mysqlDsn, err)
		return
	}

	baseField := []string{"start_time", "duration"}

	startPapersKey := "sx_today_mock_papers"
	opt := &redis.ZRangeBy{Min: "0", Max: "0.0"}

	var workPool *libary.WorkPool = libary.NewWorkPool(poolNum, jobLen, resLen)

	myTimer := time.NewTicker(time.Second)

	processAnswers := func(args ...interface{}) error {
		defer func() {
			if err := recover(); err != nil {
				loggers.Printf("[%s] 出现异常错误,error:%v\n", "error", err)
			}
		}()

		if len := len(args); len < 1 {
			return errors.New("参数错误")
		}

		workIndex := args[len(args)-1].(int)

		answer, ok := args[0].(string)
		if !ok {
			return fmt.Errorf("work_%d answer数据类型转换失败", workIndex)
		}

		loggers.Printf("[%s] work_%d json数据: %s\n", "info", workIndex, answer)

		var mock model.Mock
		err := json.Unmarshal([]byte(answer), &mock)
		if err != nil {
			loggers.Printf("[%s] work_%d %s json数据解析失败,origin:%s %v\n", "error", workIndex, answer, args[0], err)
			return err
		}

		db, ok := args[1].(*sql.DB)
		if !ok {
			return fmt.Errorf("work_%d db数据类型转换失败", workIndex)
		}

		err = mock.ConsumData(db)
		if err != nil {
			loggers.Printf("[%s] work_%d 写入数据库失败,origin:%v %v\n", "error", workIndex, mock, err)
			return err
		}

		return nil
	}

	processStat := func(args ...interface{}) error {
		defer func() {
			if err := recover(); err != nil {
				loggers.Printf("[%s] 出现异常错误,error:%v\n", "error", err)
			}
		}()

		if len := len(args); len < 1 {
			return errors.New("参数错误")
		}

		workIndex := args[len(args)-1].(int)

		examID, ok := args[0].(string)
		if !ok {
			return fmt.Errorf("work_%d examID数据类型转换失败", workIndex)
		}

		paperID, err := strconv.ParseInt(examID, 10, 64)
		if err != nil {
			loggers.Printf("[%s] work_%d %v 转换成int64失败,%v\n", "error", workIndex, examID, err)
			return err
		}

		loggers.Printf("[%s] work_%d paper_id: %v\n", "info", workIndex, paperID)

		db, ok := args[1].(*sql.DB)
		if !ok {
			return fmt.Errorf("work_%d db数据类型转换失败", workIndex)
		}

		mock := &model.Mock{}
		err = mock.UpdateStat(paperID, db)
		if err != nil {
			loggers.Printf("[%s] work_%d %v 更新统计信息失败,%v\n", "error", workIndex, paperID, err)
			fmt.Println(err)
			return err
		}

		return nil
	}

	workPool.Run()

	for {
		now := <-myTimer.C
		current = now.Unix()
		limit = strconv.FormatFloat(float64(current), 'f', 2, 64)
		opt.Max = limit
		papers, err := client.ZRangeByScoreWithScores(startPapersKey, opt).Result()
		if err != nil {
			loggers.Printf("[%s] redis 服务出问题了\n", "info")
			break
		}

		if num := len(papers); num < 1 {
			loggers.Printf("[%s] 没有模考交卷队列数据要处理\n", "info")
			continue
		}

		data = make([]string, 0)
		statArr = make([]string, 0)
		for _, v := range papers {
			paperID := v.Member.(string)
			paperKey = fmt.Sprintf("sx_mock_base_%s", paperID)
			listKey = fmt.Sprintf("sx_mock_answer_list_%s", paperID)
			flag := client.Exists(paperKey).Val()
			listFlag := client.Exists(listKey).Val()
			if flag == 0 {
				client.ZRem(startPapersKey, paperID).Result()
				statArr = append(statArr, paperID)
				continue
			} else {
				paperInfo := client.HMGet(paperKey, baseField...).Val()
				startTime, _ = strconv.ParseInt(paperInfo[0].(string), 10, 64)
				duration, _ = strconv.ParseInt(paperInfo[1].(string), 10, 64)
				if listFlag == 0 && ((startTime + duration) < current) {
					statArr = append(statArr, paperID)
					client.ZRem(startPapersKey, paperID).Result()
					continue
				}
			}

			if listFlag == 1 {
				i := 1
				for {
					if i >= listSize {
						break
					}

					row, err := client.LPop(listKey).Result()
					if err != nil {
						loggers.Printf("[%s] key:%s %v\n", "info", listKey, err)
						break
					}

					data = append(data, row)
					i++
				}
			}

		}

		loggers.Printf("[%s] data len:%d\n", "info", len(data))
		fmt.Println(current, data, len(data))
		if dataNum := len(data); dataNum >= 1 {
			go func(data []string, workPool *libary.WorkPool) {
				for _, m := range data {
					go func(answer string) {
						params := make([]interface{}, 2)
						params[0] = answer
						params[1] = db
						task := &libary.Task{
							F:      processAnswers,
							Params: params,
						}
						go workPool.AddTask(task)
					}(m)
				}
			}(data, workPool)
		}

		if statNum := len(statArr); statNum >= 1 {
			go func(stat_arr []string, workPool *libary.WorkPool) {
				for _, m := range stat_arr {
					go func(workPool *libary.WorkPool, paperID string) {
						params := make([]interface{}, 2)
						params[0] = paperID
						params[1] = db
						task := &libary.Task{
							F:      processStat,
							Params: params,
						}
						go workPool.AddTask(task)
					}(workPool, m)
				}
			}(statArr, workPool)
		}
	}
	/*
		data := make([]string, 19999)
		for i := range data {
			data[i] = fmt.Sprintf("%s_%d", "xiaoming", i)
		}

		var workPool = NewWorkPool(poolNum, jobLen, resLen)
		go func() {
			for _, v := range data {
				go func(workPool *WorksPool, name string) {
					params := make([]interface{}, 1)
					params[0] = name
					task := &Task{
						f: func(args ...interface{}) error {
							name := args[0].(string)
							i := args[1].(int)
							fmt.Printf("worker:%d name:%s\n", i, name)
							return nil
						},
						params: params,
					}
					go workPool.AddTask(task)
				}(workPool, v)
			}
		}()
		workPool.Run()
		for {

		}
	*/
}
