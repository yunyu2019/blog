package main

import (
	"fmt"
	"reflect"
)

// Stu 学生结构体
type Stu struct {
	Name  string
	Age   uint8
	Score []float64
}

// NewStu 创建一个新的stu结构
func NewStu(name string, age uint8, score []float64) *Stu {
	return &Stu{
		Name:  name,
		Age:   age,
		Score: score,
	}
}

func (stu *Stu) SetName(name string) bool {
	stu.Name = name
	return true
}

func (stu *Stu) GetName() string {
	return stu.Name
}

func main() {
	scores := []float64{90.5, 60.8, 70.5}
	stu := NewStu("小明", 20, scores)
	v := reflect.ValueOf(stu)
	s := make([]reflect.Value, 1)
	s[0] = reflect.ValueOf("小花")
	v.MethodByName("SetName").Call(s)

	s1 := make([]reflect.Value, 0)
	r := v.MethodByName("GetName").Call(s1)
	fmt.Println(r[0].String())

}
