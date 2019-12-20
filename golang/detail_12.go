/*
 * Author: yunyu2019
 * Date: 2019-12-16 18:13:43
 * Description:
 */
package main

import (
	"fmt"
	"sync"
)

type S struct {
	name string
}

func main() {
	m := make(map[int]int)
	wg := &sync.WaitGroup{}
	mu := &sync.Mutex{}
	wg.Add(10)
	for i := 0; i < 10; i++ {
		go func(i int) {
			defer wg.Done()
			mu.Lock()
			m[i] = i
			mu.Unlock()
		}(i)
	}
	wg.Wait()
	for k, v := range m {
		fmt.Println(k, v)
	}
	fmt.Println("----------------------------")
	s := map[string]S{"x": S{"one"}}
	fmt.Println(s)
	//s["x"].name = "two" //cannot assign to struct field s["x"].name in map
	x := s["x"]
	x.name = "two"
	s["x"] = x
	fmt.Println(s)
}
