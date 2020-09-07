/*
 * Author: yunyu2019
 * Date: 2019-12-13 13:57:08
 * Description:
 */
package main

import (
	"encoding/json"
	"fmt"
	"time"
)

type Slice []int

func NewSlice() Slice {
	return make(Slice, 0)
}

func (s *Slice) Add(elem int) *Slice {
	*s = append(*s, elem)
	fmt.Print(elem)
	return s
}

func main() {
	items := make(map[string]string)
	items["name"] = "小明"
	items["sex"] = "man"
	data, _ := json.Marshal(items)
	s := string(data)
	fmt.Println(s)
	var item map[string]string
	json.Unmarshal([]byte(s), &item)
	fmt.Println(item)

	fmt.Println("--------------------------------")

	strs := []string{"one", "two", "three"}
	for _, s := range strs {
		go func() {
			time.Sleep(1 * time.Second)
			fmt.Printf("%s ", s)
		}()
	}
	time.Sleep(3 * time.Second)

	fmt.Println("\n--------------------------------")
	S := NewSlice()
	defer S.Add(1).Add(2)
	S.Add(3)
}
