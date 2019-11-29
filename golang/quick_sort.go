/*
* 快速排序
 */
package main

import (
	"fmt"
)

func quickSort(left int, right int, arr *[14]int) {
	fmt.Println(arr)
	index := (left + right) / 2
	pivot := arr[index]
	start := left
	end := right
	fmt.Println("middle:", arr[index])
	for start < end {
		//从右边指针查找比pivot小的数据，直到找到为止，找不到就一直向左移动右指针
		for arr[end] > pivot {
			end--
		}

		//从做边查找比pivot大的数据，直到找到为止，找不到就一直向右移动左指针
		for arr[start] < pivot {
			start++
		}

		//左右指针重合就结束本次查找
		if start >= end {
			break
		}

		//同时找到了比pivot小的数据及比pivot大的数据，然后进行两者交换
		arr[start], arr[end] = arr[end], arr[start]
		if arr[start] == pivot {
			end--
		}
		if arr[end] == pivot {
			start++
		}
	}
	if start == end {
		start++
		end--
	}
	//以pivot位置为基准，向左递归排序
	if left < end {
		quickSort(left, end, arr)
	}

	//以pivot位置为基准，向右递归排序
	if right > start {
		quickSort(start, right, arr)
	}
}

func main() {
	arr := [...]int{49, 38, 65, 97, 23, 22, 76, 1, 5, 8, 2, 0, -1, 22}
	quickSort(0, len(arr)-1, &arr)
	fmt.Println(arr)
}
