package libary

import "fmt"

// Task 任务结构
type Task struct {
	F      func(args ...interface{}) error
	Params []interface{}
}

// WorkPool 协程池
type WorkPool struct {
	JobChan chan *Task
	Num     int
	ResChan chan string
}

// NewWorkPool 创建协程池
func NewWorkPool(num int, jobLen int, resLen int) *WorkPool {
	return &WorkPool{
		JobChan: make(chan *Task, jobLen),
		ResChan: make(chan string, resLen),
		Num:     num,
	}
}

// AddTask 协程池添加任务
func (workPool *WorkPool) AddTask(task *Task) error {
	workPool.JobChan <- task
	return nil
}

// Run 运行协程池
func (workPool *WorkPool) Run() {
	for i := 1; i <= workPool.Num; i++ {
		go func(i int) {
			for {
				task, ok := <-workPool.JobChan
				if !ok {
					fmt.Printf("work_%d job chan 通道已关闭\n", i)
					continue
				}

				task.Params = append(task.Params, i)
				err := task.F(task.Params...)
				if err != nil {
					fmt.Println(err)
					continue
				}
			}
		}(i)
	}
}
