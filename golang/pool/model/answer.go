package model

// CommonAnswer 公共结果结构体
type CommonAnswer struct {
	UserID     int64   `json:"user_id"`
	Score      float64 `json:"score"`
	Duration   uint32  `json:"duration"`
	BeginTime  int64   `json:"begin_time"`
	CreateAt   int64   `json:"create_at"`
	Source     uint8   `json:"source"`
	WrongNum   uint16  `json:"wrong_num"`
	CorrectNum uint16  `json:"correct_num"`
	UndoNum    uint16  `json:"undo_num"`
	Answers    []Quest `json:"answers"`
}
