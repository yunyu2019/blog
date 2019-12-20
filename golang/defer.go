package main

import (
	"fmt"
	"log"
	"time"
)

func gee() func(s string) string {
	msg := time.Now().Unix()
	return func(s string) string {
		a := fmt.Sprintf("%d %s", msg, s)
		fmt.Println(a)
		return a
	}
}
func main() {
	f := gee()
	defer f("123")
	f("456")
	fmt.Println("lala")
	bigSlowOperation()
}

func bigSlowOperation() {
	defer trace("bigSlowOperation")() // don't forget the extra parentheses   // ...lots of work…
	time.Sleep(3 * time.Second)      // simulate slow operation by sleeping
}

func trace(msg string) func() {
	start := time.Now()
	log.Printf("enter %s", msg)
	return func() {
		log.Printf("exit %s (%s)", msg, time.Since(start))
	}
}
