/*
 * Author: yunyu2019
 * Date: 2019-12-16 11:26:01
 * Description:
 */
//使用接口作为函数入参/返回值时，如果实际传递/返回的是nil子类对象，那么这一入参/返回值接口对象依然是不为nil的，接口对象的内在结构必须令其能够支持潜在的类型断言或抽象方法调用，一个完全为nil的接口对象是无法做到这一点的；
package main

import (
	"fmt"
)

type People3 interface {
	Show()
}

type Student struct{}

func (stu *Student) Show() {}

func live() People3 {
	var stu *Student
	fmt.Println(stu)
	return stu
}

func main() {
	people3 := live()
	fmt.Printf("people3 %T %v\n", people3, people3)
	if people3 == nil {
		fmt.Println("AAAAAAA")
	} else {
		fmt.Println("BBBBBBB") //返回
	}

	fmt.Println("-----------------------------")
	var stu *Student
	people4 := stu //返回AAAAAAA
	//people4 := People3(stu) //返回BBBBBBB
	fmt.Printf("people4 %T %v\n", people4, people4)
	if people4 == nil {
		fmt.Println("AAAAAAA")
	} else {
		fmt.Println("BBBBBBB")
	}
}
