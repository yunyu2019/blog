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

	"github.com/go-redis/redis/v7"
	"github.com/go-sql-driver/mysql"
)

// Quest 答案结构体
type Quest struct {
	QuestID      string `json:"quest_id"`
	MyAnswer     string `json:"my_answer"`
	AnswerStatus uint8  `json:"answer_status"`
	MarkFlag     uint8  `json:"mark_flag"`
}

// Answer 答题结果结构体
type Answer struct {
	UserID     int64   `json:"user_id"`
	ExamID     int64   `json:"exam_id"`
	Score      float64 `json:"score"`
	Duration   uint32  `json:"duration"`
	BeginTime  int64   `json:"begin_time"`
	AnswerAt   int64   `json:"answer_at"`
	CreateAt   int64   `json:"create_at"`
	Source     uint8   `json:"source"`
	WrongNum   uint16  `json:"wrong_num"`
	CorrectNum uint16  `json:"correct_num"`
	UndoNum    uint16  `json:"undo_num"`
	Answers    []Quest `json:"answers"`
}

// WorkPool 协程池结构体
type WorkPool struct {
	JobChan chan string
	WorkNum int
}

// AddTask 添加数据到协程池
func (workPool *WorkPool) AddTask(data string) error {
	workPool.JobChan <- data
	return nil
}

// Run 协程池处理任务
func (workPool *WorkPool) Run(db *sql.DB) {
	for i := 1; i <= workPool.WorkNum; i++ {
		go func(i int, db *sql.DB) {
			for {
				answer, ok := <-workPool.JobChan
				loggers.Println(answer)
				if !ok {
					loggers.Printf("[%s] mock_answer_worker_%d %s\n", "info", i, "answer_chan 通道已关闭")
					continue
				}

				if answer == "" {
					loggers.Printf("[%s] mock_answer_worker_%d %s\n", "info", i, "answer_chan 通道已无数据")
					continue
				}
				err := processAnswers(i, db, answer)
				if err != nil {
					fmt.Println(err)
					continue
				}
			}
		}(i, db)
	}
}

// processAnswer 处理答题结果记录
func processAnswers(i int, db *sql.DB, answer string) error {
	info := fmt.Sprintf("mock_answer_worker_%d\n", i)
	loggers.Println(info)
	var myAnswer Answer
	err := json.Unmarshal([]byte(answer), &myAnswer)
	if err != nil {
		fmt.Println(err)
		loggers.Printf("[%s] %s json数据解析失败,origin:%s %v\n", "error", info, answer, err)
		return err
	}

	err = myAnswer.insertAnswer(db)
	if err != nil {
		fmt.Println(err)
		loggers.Printf("[%s] %s 写入数据库失败,origin:%v %v\n", "error", info, myAnswer, err)
		return err
	}

	return nil
}

// processStat 处理试题统计
func processStat(channel chan string, i int, group int, db *sql.DB) error {
	info := fmt.Sprintf("group:%d mock_stat_%d", group, i)
	fmt.Println(info)
	examID, ok := <-channel
	if !ok {
		loggers.Printf("[%s] %s %s\n", "info", info, "stat_chan 通道已关闭")
		return errors.New("stat_chan 通道已关闭")
	}

	paperID, err := strconv.ParseInt(examID, 10, 64)
	if err != nil {
		loggers.Printf("[%s] %s %v 转换成int64失败,%v\n", "error", info, examID, err)
		return err
	}

	err = updateStats(paperID, db)
	if err != nil {
		loggers.Printf("[%s] %s %v 更新统计信息失败,%v\n", "error", info, paperID, err)
		fmt.Println(err)
		return err
	}

	return nil
}

// insertAnswer 写入答案记录
func (myAnswer *Answer) insertAnswer(db *sql.DB) error {
	correctRate := fmt.Sprintf("%.2f", float64(myAnswer.CorrectNum*100)/float64(myAnswer.CorrectNum+myAnswer.WrongNum+myAnswer.UndoNum))
	answers, _ := json.Marshal(myAnswer.Answers)

	answerIns, err := db.Prepare("insert into mock_user_answer (`paper_id`,`user_id`,`answers`,`score`,`correct_num`,`wrong_num`,`undo_num`,`correct_rate`,`answer_dura`,`submit_at`,`create_at`,`source`) values (?,?,?,?,?,?,?,?,?,?,?,?)")
	if err != nil {
		return err
	}

	_, err = answerIns.Exec(myAnswer.ExamID, myAnswer.UserID, string(answers), myAnswer.Score, myAnswer.CorrectNum, myAnswer.WrongNum, myAnswer.UndoNum, correctRate, myAnswer.Duration, myAnswer.AnswerAt, myAnswer.CreateAt, myAnswer.Source)
	if err != nil {
		answerIns.Close()
		return err
	}

	answerIns.Close()

	enrollOut, err := db.Prepare("select province_id from mock_enroll where user_id = ? and paper_id = ? limit 1")
	if err != nil {
		return err
	}

	var provinceID sql.NullInt64
	err = enrollOut.QueryRow(myAnswer.UserID, myAnswer.ExamID).Scan(&provinceID)
	if err != nil && err != sql.ErrNoRows {
		enrollOut.Close()
		return err
	}

	var province int64
	if provinceID.Valid {
		province = provinceID.Int64
	}

	enrollOut.Close()

	rankIns, err := db.Prepare("insert into mock_ranking (`estate`,`paper_id`,`user_id`,`province_id`,`score`,`create_at`) values (?,?,?,?,?,?)")
	if err != nil {
		return err
	}

	_, err = rankIns.Exec(1, myAnswer.ExamID, myAnswer.UserID, province, myAnswer.Score, myAnswer.CreateAt)
	if err != nil {
		rankIns.Close()
		return err
	}
	rankIns.Close()
	return nil
}

// updateStat 更新平均分及参考人数
func updateStats(paperID int64, db *sql.DB) error {
	avgOut, err := db.Prepare("select avg(score) as avg_score from mock_user_answer where paper_id = ?")
	if err != nil {
		return err
	}

	var avgScore sql.NullFloat64
	err = avgOut.QueryRow(paperID).Scan(&avgScore)
	if err != nil && err != sql.ErrNoRows {
		avgOut.Close()
		return err
	}

	score, _ := avgScore.Value()
	avgOut.Close()

	updateSQL := "update mock_paper set report_flag = ?"
	if score != nil {
		updateSQL += fmt.Sprintf(",avg_score = %.2f", score)
	}
	updateSQL += " where id = ?"

	upIns, err := db.Prepare(updateSQL)
	if err != nil {
		return err
	}

	_, err = upIns.Exec(1, paperID)
	if err != nil {
		upIns.Close()
		return err
	}

	upIns.Close()

	examOut, err := db.Prepare("select count(score) as exam_num from mock_user_answer where paper_id = ?")
	if err != nil {
		return err
	}

	var examNum sql.NullInt32
	err = examOut.QueryRow(paperID).Scan(&examNum)
	if err != nil && err != sql.ErrNoRows {
		examOut.Close()
		return err
	}

	examOut.Close()
	exam, _ := examNum.Value()

	if exam != nil {
		upIns, err := db.Prepare("update mock_paper_stat set exam_num = ?,update_at = ? where paper_id = ?")
		if err != nil {
			return err
		}

		_, err = upIns.Exec(examNum, time.Now().Unix(), paperID)
		if err != nil {
			upIns.Close()
			return err
		}

		upIns.Close()
	}
	return nil
}

var (
	loggers *log.Logger
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
	var current int64
	var max string
	var paperKey string
	var listKey string
	var startTime int64
	var duration int64
	var statArr []string
	var data []string

	var statGoCount int = 4 //处理模考统计协程数量
	var statChan chan string
	var listSize int = 100

	baseField := []string{"start_time", "duration"}

	myTimer := time.NewTicker(time.Second)

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

	startPapersKey := "sx_today_mock_papers"
	opt := &redis.ZRangeBy{Min: "0", Max: max}

	var workPool *WorkPool = &WorkPool{}
	var JobChan chan string
	JobChan = make(chan string, 100)
	workPool.JobChan = JobChan
	workPool.WorkNum = 8

	for {
		now := <-myTimer.C
		current = now.Unix()
		max = strconv.FormatFloat(float64(current), 'f', 2, 64)
		opt.Max = max
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
		statChan = make(chan string, 4)
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
			go func(data []string, workPool *WorkPool) {
				for _, m := range data {
					go workPool.AddTask(m)
				}
			}(data, workPool)
			go workPool.Run(db)
		}

		if statNum := len(statArr); statNum >= 1 {
			go func(stat_arr []string, channel chan string) {
				for _, m := range stat_arr {
					channel <- m
				}
				close(channel)
			}(statArr, statChan)

			go func(n int, channel chan string, num int) {
				s := 1
				total := num/n + 1
				for {
					if s > total {
						break
					}
					for i := 1; i <= n; i++ {
						go processStat(channel, i, s, db)
					}
					s++
				}
			}(statGoCount, statChan, statNum)
		}
	}
}
