/*
* 数组模拟环形队列
* 判断环形队列是否为空:head == tail
* 判断环形队列是否已满:(tail+1)%size == head
* 计算环形队列总长度:(tail+size -head)%size
* head移动轨迹:(head+1)%size
* tail移动轨迹:(tail+1)%size
 */
package main

import (
	"errors"
	"fmt"
	"os"
)

type CircelQueue struct {
	size  int
	data  [5]int
	first int
	last  int
}

func (this *CircelQueue) IsFull() bool {
	return (this.last+1)%this.size == this.first
}

func (this *CircelQueue) IsEmpty() bool {
	return this.last == this.first
}

func (this *CircelQueue) Size() int {
	return (this.last + this.size - this.first) % this.size
}

func (this *CircelQueue) push(a int) (err error) {
	if this.IsFull() {
		return errors.New("queue is full")
	}
	this.data[this.last] = a
	this.last = (this.last + 1) % this.size
	return
}

func (this *CircelQueue) pop() (val int, err error) {
	if this.IsEmpty() {
		return 0, errors.New("queue is empty")
	}
	val = this.data[this.first]
	this.first = (this.first + 1) % this.size
	return
}

func (this *CircelQueue) scan() {
	size := this.Size()
	if size == 0 {
		fmt.Printf("queue is empty\n")
		return
	}
	head := this.first
	for i := 0; i < size; i++ {
		fmt.Printf("this.data[%d]=%d\n", head, this.data[head])
		head = (head + 1) % this.size
	}
}

func main() {
	queue := &CircelQueue{
		size:  5,
		first: 0,
		last:  0,
	}
	fmt.Println("操作菜单如下:")
	fmt.Println("1.添加元素请输入push")
	fmt.Println("2.取出元素请输入pop")
	fmt.Println("3.查看队列所有元素,请输入show")
	fmt.Println("4.退出程序请输入exit")
	for {
		var menu string
		fmt.Scan(&menu)
		switch menu {
		case "push":
			var item int
			fmt.Print("请输入新元素:")
			fmt.Scan(&item)
			err := queue.push(item)
			if err != nil {
				fmt.Println(err.Error())
			} else {
				fmt.Println("加入队列成功")
			}
		case "pop":
			val, err := queue.pop()
			if err != nil {
				fmt.Println(err.Error())
			} else {
				fmt.Println("队列弹出元素成功", val)
			}
		case "show":
			queue.scan()
		case "size":
			size := queue.Size()
			fmt.Println("环形队列总长度为:", size)
		case "exit":
			os.Exit(0)
		}
	}
}
