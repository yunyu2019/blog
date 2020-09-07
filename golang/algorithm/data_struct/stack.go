//使用数组模拟栈
package main

import (
	"errors"
	"fmt"
)

type Stack struct {
	size int
	top  int
	data [5]int
}

func (this *Stack) push(n int) (err error) {
	if this.top == this.size-1 {
		return errors.New("堆栈已经满了")
	}
	this.top++
	this.data[this.top] = n
	return nil
}

func (this *Stack) pop() (n int, err error) {
	if this.top == -1 {
		return 0, errors.New("堆栈已空")
	}
	n = this.data[this.top]
	this.top--
	return n, nil
}

func (this *Stack) list() {
	if this.top == -1 {
		fmt.Println("堆栈已空")
		return
	}
	for i := this.top; i >= 0; i-- {
		fmt.Printf("arr[%d]=%d\n", i, this.data[i])
	}
}

func main() {
	stack := &Stack{
		size: 5,
		top:  -1,
	}
	stack.push(1)
	stack.push(2)
	stack.push(3)
	stack.push(4)
	stack.push(5)
	err := stack.push(6)
	fmt.Println(err)
	stack.list()
	n, _ := stack.pop()
	fmt.Println("弹出元素", n)
	n1, _ := stack.pop()
	fmt.Println("弹出元素", n1)
	n2, _ := stack.pop()
	fmt.Println("弹出元素", n2)
	n3, _ := stack.pop()
	fmt.Println("弹出元素", n3)
	n4, _ := stack.pop()
	fmt.Println("弹出元素", n4)
	n5, err := stack.pop()
	fmt.Println(n5, err)
	//stack.list()
}
