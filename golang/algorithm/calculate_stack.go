//栈模拟计算表达式运算过程
package main

import (
	"errors"
	"fmt"
	"strconv"
)

type Stack struct {
	size int
	top  int
	data [10]int
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

func cal(num1 int, num2 int, oper int) (res int) {
	switch oper {
	case 42:
		res = num1 * num2
	case 43:
		res = num1 + num2
	case 45:
		res = num1 - num2
	case 47:
		res = num1 / num2
	default:
		res = -1
	}
	return
}

func isOper(n int) bool {
	if n == 42 || n == 43 || n == 45 || n == 47 {
		return true
	}
	return false
}

func priority(oper int) int {
	level := 0
	switch oper {
	case 42:
		fallthrough
	case 47:
		level = 2
	case 43:
		fallthrough
	case 45:
		level = 1
	}
	return level
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
	//数字栈
	num_stack := &Stack{
		size: 10,
		top:  -1,
	}

	//符号栈
	oper_stack := &Stack{
		size: 10,
		top:  -1,
	}
	exp := "3+20*6-20"
	num1 := 0
	num2 := 0
	keep := ""
	for i, num := 0, len(exp); i < num; i++ {
		data := int(exp[i])
		if isOper(data) {
			level := priority(data)
			fmt.Printf("%d level:%d\n", data, level)
			if oper_stack.top == -1 {
				oper_stack.push(data)
			} else {
				level2 := priority(oper_stack.data[oper_stack.top])
				if level2 >= level {
					num2, _ = num_stack.pop()
					num1, _ = num_stack.pop()
					oper, _ := oper_stack.pop()
					res := cal(num1, num2, oper)
					fmt.Printf("%d %s %d = %d\n", num1, string(oper), num2, res)
					num_stack.push(res)
					oper_stack.push(data)
				} else {
					oper_stack.push(data)
				}
			}
		} else {
			keep += string(data)
			if i == num-1 {
				n, _ := strconv.Atoi(keep)
				num_stack.push(n)
				fmt.Printf("push num stack: %d\n", n)
			} else {
				if isOper(int(exp[i+1])) {
					n, _ := strconv.Atoi(keep)
					num_stack.push(n)
					keep = ""
					fmt.Printf("push num stack: %d\n", n)
				}
			}
		}
	}
	for {
		if oper_stack.top == -1 {
			break
		}
		oper, _ := oper_stack.pop()
		num2, _ = num_stack.pop()
		num1, _ = num_stack.pop()
		res := cal(num1, num2, oper)
		num_stack.push(res)
	}
	if num_stack.top != -1 {
		res, _ := num_stack.pop()
		fmt.Printf("exp:%s = %d\n", exp, res)
	}

}
