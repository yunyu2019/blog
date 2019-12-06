//hash表实现
package main

import (
	"fmt"
	"os"
)

type Employee struct {
	id   int
	name string
	next *Employee
}

type Emplink struct {
	head *Employee
}

func (this *Emplink) insert(emp *Employee) {
	curr := this.head
	if curr == nil {
		this.head = emp
		return
	}
	var pre *Employee = nil
	flag := true
	for {
		if curr == nil {
			break
		}

		if curr.id > emp.id {
			break
		} else if curr.id == emp.id {
			flag = false
		}
		pre = curr
		curr = curr.next
	}

	if !flag {
		fmt.Println("数据已存在")
		return
	}

	if pre != nil {
		pre.next = emp
	} else {
		this.head = emp
	}
	emp.next = curr
}

func (this *Emplink) show() (emps []Employee) {
	if this.head == nil {
		fmt.Println("nil")
		return
	}
	curr := this.head
	for {
		if curr == nil {
			break
		}
		emps = append(emps, *curr)
		curr = curr.next
	}
	return
}

func (this *Emplink) find(n int) (emp *Employee) {
	if this.head == nil {
		return nil
	}
	temp := this.head
	flag := false
	for {
		if temp == nil {
			break
		}
		if temp.id == n {
			flag = true
			break
		}
		temp = temp.next
	}
	if !flag {
		return nil
	}
	return temp
}

type HashTable struct {
	Linkarr [7]Emplink
}

func (this *HashTable) HashFun(n int) int {
	return n % 7
}

func (this *HashTable) insert(emp *Employee) {
	num := this.HashFun(emp.id)
	this.Linkarr[num].insert(emp)
}

func (this *HashTable) show() {
	for i, num := 0, len(this.Linkarr); i < num; i++ {
		fmt.Printf("链表%d=>", i)
		emps := this.Linkarr[i].show()
		for _, emp := range emps {
			fmt.Print(emp, " => ")
		}
		fmt.Println()
	}
}

func (this *HashTable) find(n int) (num int, emp *Employee) {
	num = this.HashFun(n)
	emp = this.Linkarr[num].find(n)
	return
}

func main() {
	fmt.Println("雇员信息菜单")
	fmt.Println("添加雇员:add")
	fmt.Println("查找雇员:select")
	fmt.Println("显示雇员:show")
	fmt.Println("退出菜单:exit")
	var key string
	var hash HashTable
	var id int
	var name string
	for {
		fmt.Println("请输入菜单项")
		fmt.Scan(&key)
		switch key {
		case "add":
			fmt.Print("请输入雇员id:")
			fmt.Scan(&id)
			fmt.Print("请输入雇员名称:")
			fmt.Scan(&name)
			emp := &Employee{
				id:   id,
				name: name,
			}
			hash.insert(emp)
		case "show":
			hash.show()
		case "find":
			fmt.Print("请输入雇员id:")
			fmt.Scan(&id)
			num, emp := hash.find(id)
			if emp == nil {
				fmt.Printf("id %d 的数据不存在\n", id)
			} else {
				fmt.Printf("在链表 %d 找到了数据%v\n", num, emp)
			}
		case "exit":
			os.Exit(0)
		}
	}
}
