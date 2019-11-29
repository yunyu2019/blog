/*
* 插入排序
 */
package main

import (
	"fmt"
)

func InserSort(arr *[7]int) {
	/*
		* 插入排序分析过程
		//第一次排序
		val := arr[1]
		index := 1 - 1
		for index >= 0 && arr[index] < val {
			arr[index+1] = arr[index]
			index--
		}
		if index+1 != 1 {
			arr[index+1] = val
		}
		fmt.Println("第1次排序结果:", *arr)

		//第二次排序
		val = arr[2]
		index = 2 - 1
		for index >= 0 && arr[index] < val {
			arr[index+1] = arr[index]
			index--
		}
		if index+1 != 2 {
			arr[index+1] = val
		}
		fmt.Println("第2次排序结果:", *arr)

		//第三次排序
		val = arr[3]
		index = 3 - 1
		for index >= 0 && arr[index] < val {
			arr[index+1] = arr[index]
			index--
		}
		if index+1 != 3 {
			arr[index+1] = val
		}
		fmt.Println("第3次排序结果:", *arr)

		//第四次排序
		val = arr[4]
		index = 4 - 1
		for index >= 0 && arr[index] < val {
			arr[index+1] = arr[index]
			index--
		}
		if index+1 != 4 {
			arr[index+1] = val
		}
		fmt.Println("第4次排序结果:", *arr)
	*/
	for i, lens := 1, len(arr); i < lens; i++ {
		val := arr[i]
		index := i - 1
		for index >= 0 && arr[index] < val {
			arr[index+1] = arr[index]
			index--
		}
		if index+1 != i {
			arr[index+1] = val
		}
		fmt.Printf("第%d次排序结果:%v\n", i, *arr)
	}

}

func main() {
	arr := [7]int{23, 0, 12, 56, 34, -1, 55}
	fmt.Println(arr)
	InserSort(&arr)
	fmt.Println(arr)
}
