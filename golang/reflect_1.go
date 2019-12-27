package main

import (
	"encoding/json"
	"fmt"
	"reflect"
)

//testReflect 利用反射创建一个结构体并完成初始化工作
func testReflect() {
	ptype := reflect.StructOf([]reflect.StructField{
		{
			Name:      "Name",
			Type:      reflect.TypeOf(""),
			Tag:       `json:"name"`,
			Anonymous: false,
		},
		{
			Name:      "Age",
			Type:      reflect.TypeOf(int(0)),
			Tag:       `json:"age"`,
			Anonymous: false,
		},
		{
			Name:      "Sex",
			Type:      reflect.TypeOf(uint8(0)),
			Tag:       `json:"sex"`,
			Anonymous: false,
		},
		{
			Name:      "Score",
			Type:      reflect.TypeOf(int(0)),
			Tag:       `json:"score"`,
			Anonymous: false,
		},
	})
	p := reflect.New(ptype)
	model := p.Elem()
	model.FieldByName("Name").SetString("小明")
	model.FieldByName("Age").SetInt(20)
	model.FieldByName("Sex").SetUint(1)
	model.FieldByName("Score").SetInt(80)
	fmt.Println(p, model)
	data, err := json.Marshal(model.Interface())
	if err != nil {
		fmt.Println(err)
		return
	}
	fmt.Println(string(data))
}

func main() {
	testReflect()
}
