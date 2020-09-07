/*
 * Author: yunyu2019
 * Date: 2019-12-16 10:21:07
 * Description:
 */
package main

import (
	"fmt"
	"runtime"
	"sync"
)

func main() {
	runtime.GOMAXPROCS(1)
	wg := sync.WaitGroup{}

	wg.Add(10)

	for i := 0; i < 5; i++ {
		go func() {
			fmt.Println("A: ", i)
			wg.Done()
		}()
	}

	for i := 0; i < 5; i++ {
		go func(i int) {
			fmt.Println("B: ", i)
			wg.Done()
		}(i)
	}

	wg.Wait()
}
