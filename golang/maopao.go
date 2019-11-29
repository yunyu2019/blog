//冒泡排序
package main

import (
	"fmt"
)

func maopao1(a []int) []int {
	for i, len := 0, len(a); i < len; i++ {
		for j := i + 1; j < len; j++ {
			if a[i] < a[j] {
				a[i], a[j] = a[j], a[i]
			}
		}
	}
	return a
}

func maopao2(a []int) []int {
	len := len(a)
	for i := 0; i <= len-1; i++ {
		for j := 0; j < len-i-1; j++ {
			if a[j] > a[j+1] {
				a[j], a[j+1] = a[j+1], a[j]
			}
		}
	}
	return a
}

func main() {
	a := []int{2, 5, 4, 6, 9, 7, 1}
	maopao1(a)
	//maopao2(a)
	fmt.Println(a)
}
