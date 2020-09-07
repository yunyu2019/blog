/*
*二分查找数组元素
*前提:数组是一个从小到大的有序数组
 */
package main

import (
	"fmt"
)

//递归函数实现二分查找算法
func binarrySearch(arr []int, left int, right int, find int) int {
	if left > right {
		return -1
	}
	middle := (left + right) / 2
	if arr[middle] > find {
		return binarrySearch(arr, left, middle-1, find)
	} else if arr[middle] < find {
		return binarrySearch(arr, middle+1, right, find)
	} else {
		return middle
	}
}

//for loop实现二分查找算法
func binarrySearch2(arr []int, find int) int {
	index := -1
	left, right := 0, len(arr)-1
Loop:
	for {
		if left > right {
			break Loop
		}
		middle := (left + right) / 2
		switch true {
		case arr[middle] > find:
			right = middle - 1
		case arr[middle] < find:
			left = middle + 1
		case arr[middle] == find:
			index = middle
			break Loop
		}
	}
	return index
}

func main() {
	a := []int{1, 8, 10, 89, 1000, 1024}
	//index := binarrySearch(a, 0, len(a)-1, 500)
	index := binarrySearch2(a, 89)
	fmt.Println(index)
}
