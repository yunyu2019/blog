package model

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"time"
)

// Mock 答题结果结构体
type Mock struct {
	CommonAnswer
	AnswerAt int64 `json:"answer_at"`
	ExamID   int64 `json:"exam_id"`
}

func (mock *Mock) ConsumData(db *sql.DB) error {
	err := mock.insertAnswer(db)
	if err != nil {
		return err
	}

	provinceID, err := mock.selectEnroll(db)
	if err != nil {
		fmt.Println(err)
	}
	err = mock.insertRank(db, provinceID)
	return err
}

// insertAnswer 写入答案记录
func (mock *Mock) insertAnswer(db *sql.DB) error {
	correctRate := fmt.Sprintf("%.2f", float64(mock.CorrectNum*100)/float64(mock.CorrectNum+mock.WrongNum+mock.UndoNum))
	answers, _ := json.Marshal(mock.Answers)

	answerIns, err := db.Prepare("insert into mock_user_answer (`paper_id`,`user_id`,`answers`,`score`,`correct_num`,`wrong_num`,`undo_num`,`correct_rate`,`answer_dura`,`submit_at`,`create_at`,`source`) values (?,?,?,?,?,?,?,?,?,?,?,?)")
	if err != nil {
		return err
	}

	_, err = answerIns.Exec(mock.ExamID, mock.UserID, string(answers), mock.Score, mock.CorrectNum, mock.WrongNum, mock.UndoNum, correctRate, mock.Duration, mock.AnswerAt, mock.CreateAt, mock.Source)
	if err != nil {
		answerIns.Close()
		return err
	}

	answerIns.Close()
	return nil
}

// SelectEnroll 查询报名省份信息
func (mock *Mock) selectEnroll(db *sql.DB) (int64, error) {
	enrollOut, err := db.Prepare("select province_id from mock_enroll where user_id = ? and paper_id = ? limit 1")
	if err != nil {
		return 0, err
	}

	var provinceID sql.NullInt64
	err = enrollOut.QueryRow(mock.UserID, mock.ExamID).Scan(&provinceID)
	if err != nil && err != sql.ErrNoRows {
		enrollOut.Close()
		return 0, err
	}

	var province int64
	if provinceID.Valid {
		province = provinceID.Int64
	}

	enrollOut.Close()
	return province, nil
}

//insertRank 写入排行
func (mock *Mock) insertRank(db *sql.DB, province int64) error {
	rankIns, err := db.Prepare("insert into mock_ranking (`estate`,`paper_id`,`user_id`,`province_id`,`score`,`create_at`) values (?,?,?,?,?,?)")
	if err != nil {
		return err
	}

	_, err = rankIns.Exec(1, mock.ExamID, mock.UserID, province, mock.Score, mock.CreateAt)
	if err != nil {
		rankIns.Close()
		return err
	}
	rankIns.Close()
	return nil
}

//UpdateStat 更新模考统计
func (mock *Mock) UpdateStat(paperID int64, db *sql.DB) error {
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
