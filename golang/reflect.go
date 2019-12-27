package main

import (
	"fmt"
	"reflect"
)

//People 结构体
type People struct {
	Name  string `json:"name" form:"username"`
	Age   int    `json:"age"`
	Sex   uint8  `json:"sex"`
	score int
}

//GetName 获取people.name
func (p People) GetName() string {
	return p.Name
}

//GetAge 获取people.age
func (p People) GetAge() int {
	return p.Age
}

//SetName 设置people的name
func (p People) SetName(name string) string {
	p.Name = name
	return name
}

//SetAge 设置people的age
func (p *People) SetAge(age int) int {
	p.Age = age
	return age
}

//SetScore 设置people的score
func (p *People) SetSore(score int) int {
	p.score = score
	return score
}

func testReflect(a interface{}) {
	t := reflect.TypeOf(a)
	v := reflect.ValueOf(a)
	if v.Kind() != reflect.Struct {
		fmt.Println("不是一个结构体")
		return
	}
	//获取值反射的字段个数
	num := v.NumField()
	for i := 0; i < num; i++ {
		fmt.Printf("%s:", t.Field(i).Name)
		kind := v.Field(i).Kind()
		switch kind {
		case reflect.String:
			fmt.Printf("%s", v.Field(i).String())
		case reflect.Int:
			fmt.Printf("%d", v.Field(i).Int())
		case reflect.Uint8:
			fmt.Printf("%d", v.Field(i).Uint())
		}
		tag := t.Field(i).Tag.Get("json") //获取字段的标签
		if tag != "" {
			fmt.Printf(",tag:%s\n", t.Field(i).Tag.Get("json"))
		} else {
			fmt.Println()
		}
	}
	mnum := v.NumMethod() //获取可导出的方法数量
	for i := 0; i < mnum; i++ {
		methodName := t.Method(i).Name
		switch methodName {
		case "SetInfo":
			params := make([]reflect.Value, 0)
			newName := reflect.ValueOf("小花")
			params = append(params, newName)
			newAge := reflect.ValueOf(20)
			params = append(params, newAge)
			res := v.Method(i).Call(params)
			fmt.Printf("method:%s,new name:%s,new age:%d\n", methodName, res[0].String(), res[1].Int())
		case "GetAge":
			res := v.Method(i).Call(nil)
			fmt.Printf("method:%s,age:%d\n", methodName, res[0].Int())
		case "GetName":
			res := v.Method(i).Call(nil)
			fmt.Printf("method:%s,name:%s\n", methodName, res[0].String())
		}
	}
}

func testReflect2(a interface{}) {
	t := reflect.TypeOf(a)
	v := reflect.ValueOf(a)
	mnum := v.NumMethod() //获取指针可导出的方法数量
	for i := 0; i < mnum; i++ {
		methodName := t.Method(i).Name
		fmt.Println(methodName)
	}
	fmt.Println()
	t = t.Elem()
	v = v.Elem()
	if v.Kind() != reflect.Struct {
		fmt.Println("不是一个结构体")
		return
	}

	//获取值反射的字段个数
	num := v.NumField()
	for i := 0; i < num; i++ {
		fmt.Printf("%s:", t.Field(i).Name)
		kind := v.Field(i).Kind()
		switch kind {
		case reflect.String:
			fmt.Printf("%s", v.Field(i).String())
		case reflect.Int:
			fmt.Printf("%d", v.Field(i).Int())
		case reflect.Uint8:
			fmt.Printf("%d", v.Field(i).Uint())
		}
		tag := t.Field(i).Tag.Get("json") //获取字段的标签
		if tag != "" {
			fmt.Printf(",tag:%s\n", t.Field(i).Tag.Get("json"))
		} else {
			fmt.Println()
		}
	}
	mnum = v.NumMethod() //获取经过v.Elem()转换以后可导出的方法数量
	fmt.Println(mnum)
	for i := 0; i < mnum; i++ {
		methodName := t.Method(i).Name
		fmt.Println(methodName)
	}
}

func main() {
	/*
		var n int = 10
		N := reflect.TypeOf(n)
		VN := reflect.ValueOf(&n)
		fmt.Printf("var n %d,name:%s,type:%s,%v\n", n, N.Name(), N.Kind(), N)
		fmt.Printf("value n,type:%s,%v\n", VN.Kind(), VN)
		VN.Elem().SetInt(20)
		fmt.Printf("n:%d\n", n)
		fmt.Println("--------------------------")
	*/

	man := People{
		Name:  "小明",
		Age:   18,
		Sex:   1,
		score: 10,
	}
	/*
		t := reflect.TypeOf(man)
		fmt.Printf("var man,name:%s,type:%s,%v\n", t.Name(), t.Kind(), t)
		v := reflect.ValueOf(man)
		fmt.Printf("value man,type:%s\n", v.Kind())

		s := v.Interface()
		fmt.Println(s)
		if m, ok := s.(People); ok {
			fmt.Println(m.Name)
		} else {
			fmt.Println(v.Kind())
		}
	*/
	testReflect(man)
	fmt.Println("----------------------")
	testReflect2(&man)
}
