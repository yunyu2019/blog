/*
* 选择排序算法
* 思想:
* 背景:假设有一个无序的长度为n的整型数组
* 第一次排序:选择下标1到n-1中的最大值，和下标为0的值进行比较，如果比下标是0的数值大，则交换两个位置的数值
* 第二次排序:选择下标2到n-1中的最大值，和下标为1的值进行比较，如果比下标是1的数值大，则交换两个位置的数值
* 依次类推
 */
package main

import (
	"fmt"
)

func selectSort(arr *[5]int) {
	for i, n := 0, len(arr); i < n-1; i++ {
		max := arr[i]
		index := i
		for j := i + 1; j < n; j++ {
			if max < arr[j] {
				max = arr[j]
				index = j
			}
		}
		if index != i {
			arr[index], arr[i] = arr[i], arr[index]
		}
		fmt.Printf("第%d次排序结果:%v\n", i+1, *arr)
	}
}

func main() {
	arr := [5]int{10, 34, 19, 100, 80}
	fmt.Println(arr)
	selectSort(&arr)
	fmt.Println(arr)
}
