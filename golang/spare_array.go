//数据结构-稀疏数组
package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"strconv"
	"strings"
)

type item struct {
	row int
	col int
	val int
}

func TranSparse(arr *[11][11]int, file_name string) []item {
	items := make([]item, 0)
	items = append(items, item{11, 11, 0})
	for i, v := range arr {
		for j, m := range v {
			if m != 0 {
				one := item{i, j, m}
				items = append(items, one)
			}
		}
	}
	save(items, file_name)
	return items
}

func save(items []item, file_name string) (err error) {
	f, err := os.Create(file_name)
	if err != nil {
		fmt.Println("创建文件错误,", err)
		return err
	}
	defer f.Close()
	for _, m := range items {
		f.WriteString(fmt.Sprintf("%d %d %d\n", m.row, m.col, m.val))
	}
	return nil
}

func read(file_name string) (items []item, err error) {
	f, err := os.Open(file_name)
	if err != nil {
		fmt.Println("创建文件错误,", err)
		return
	}
	defer f.Close()
	reader := bufio.NewReader(f)
	for {
		s, err := reader.ReadString('\n')
		if err != nil || err == io.EOF {
			break
		}
		s = strings.TrimRight(s, "\n")
		a := strings.Split(s, " ")
		row, _ := strconv.Atoi(a[0])
		col, _ := strconv.Atoi(a[1])
		val, _ := strconv.Atoi(a[2])
		one := item{row, col, val}
		items = append(items, one)
	}
	return items, err
}

func main() {
	var arr [11][11]int
	arr[1][2] = 1
	arr[2][3] = 1
	fmt.Println("原始数组:")
	for _, v := range arr {
		for _, m := range v {
			fmt.Printf("%d ", m)
		}
		fmt.Println()
	}
	fmt.Println("转换成稀疏数组:")
	file_name := "spare_array.log"
	items := TranSparse(&arr, file_name)
	fmt.Println(items)

	fmt.Println("重新加载稀疏数组:")
	load_items, _ := read(file_name)
	fmt.Println(load_items)
	fmt.Println("恢复稀疏数组的数据:")
	var arr1 [11][11]int
	for i, v := range load_items {
		if i == 0 {
			continue
		}
		arr1[v.row][v.col] = v.val
	}
	for _, v := range arr1 {
		for _, m := range v {
			fmt.Printf("%d ", m)
		}
		fmt.Println()
	}
}
