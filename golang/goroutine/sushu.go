//输出素数
package main

import (
	"fmt"
)

func setNum(n int, ch chan int) {
	for i := 2; i <= n; i++ {
		ch <- i
	}
	close(ch)
}

func getNum(ch chan int, out chan int, flag chan bool) {
	var n bool
	for {
		v, ok := <-ch
		if !ok {
			break
		}
		n = true
		for i := 2; i < v; i++ {
			if v%i == 0 {
				n = false
				break
			}
		}
		if n {
			out <- v
		}
	}
	flag <- true
}

func main() {
	num := 1000
	ch := make(chan int, 1000)
	out := make(chan int, 1000)
	flags := make(chan bool, 4)
	go setNum(num, ch)
	for i := 0; i < 4; i++ {
		go getNum(ch, out, flags)
	}
	go func() {
		for i := 0; i < 4; i++ {
			<-flags
		}
		close(out)
	}()
	for v := range out {
		fmt.Println(v)
	}
}
