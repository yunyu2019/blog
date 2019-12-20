package main

import "fmt"

type student struct {
	Name string
	Age  int
}

func main() {
	m := make(map[string]*student)

	stus := []student{
		{Name: "zhou", Age: 24},
		{Name: "li", Age: 23},
		{Name: "wang", Age: 22},
	}

	/*
		for -,stu := range stus {
			m[stu.Name] = &stu //不能实现功能
		}
	*/

	for i := range stus {
		m[stus[i].Name] = &stus[i]
	}

	for _, v := range m {
		fmt.Println(v.Name, v.Age)
	}
}
