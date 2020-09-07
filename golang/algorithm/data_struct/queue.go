//数组模拟普通单向队列
package main

import (
	"errors"
	"fmt"
	"os"
)

type Queue struct {
	Maxsize int
	data    [5]int
	first   int
	last    int
}

func (this *Queue) push(a int) (err error) {
	if this.last == this.Maxsize-1 {
		return errors.New("queue is full")
	}
	this.last++
	this.data[this.last] = a
	return nil
}

func (this *Queue) pop() (val int, err error) {
	if this.first == this.last {
		return 0, errors.New("queue is empty")
	}
	this.first++
	val = this.data[this.first]
	return
}

func (this *Queue) scan() {
	for i := this.first + 1; i <= this.last; i++ {
		fmt.Printf("this.data[%d]=%d\n", i, this.data[i])
	}
}

func main() {
	queue := &Queue{
		Maxsize: 5,
		first:   -1,
		last:    -1,
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
		case "exit":
			os.Exit(0)
		}
	}
}
