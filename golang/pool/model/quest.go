package model

// Quest 单试题结构体
type Quest struct {
	QuestID      string `json:"quest_id"`
	MyAnswer     string `json:"my_answer"`
	AnswerStatus uint8  `json:"answer_status"`
	MarkFlag     uint8  `json:"mark_flag"`
}
