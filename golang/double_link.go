//普通(非环形)双向链表
package main

import (
	"fmt"
)

type Node struct {
	data int
	pre  *Node
	next *Node
}

//追加元素
func appendNode(head *Node, n *Node) {
	temp := head
	for {
		if temp.next == nil {
			break
		}
		temp = temp.next
	}
	temp.next = n
	n.pre = temp
}

//插入元素
func insertNode(head *Node, n *Node) {
	temp := head
	flag := true
	for {
		if temp.next == nil {
			break
		} else if temp.next.data > n.data {
			break
		} else if temp.next.data == n.data {
			flag = false
			break
		}
		temp = temp.next
	}
	if !flag {
		fmt.Println("节点数据已存在")
		return
	}
	n.next = temp.next
	n.pre = temp
	if temp.next != nil {
		temp.next.pre = n
	}
	temp.next = n
}

//删除元素
func deleteNode(head *Node, n int) {
	temp := head
	flag := false
	for {
		if temp.next == nil {
			flag = false
			break
		} else if temp.next.data == n {
			flag = true
			break
		}
		temp = temp.next
	}
	if !flag {
		fmt.Println("节点数据不存在")
		return
	}
	temp.next = temp.next.next
	if temp.next != nil {
		temp.next.pre = temp
	}
}

//顺序显示双向链表
func list(head *Node) (nodes []Node) {
	temp := head
	if temp.next == nil {
		return
	}
	for {
		if temp.next == nil {
			break
		}
		nodes = append(nodes, *temp.next)
		temp = temp.next
	}
	return
}

//逆序显示双向链表
func list1(head *Node) (nodes []Node) {
	temp := head
	if temp.next == nil {
		return
	}

	//将双向链表移动到最末尾元素
	for {
		if temp.next == nil {
			break
		}
		temp = temp.next
	}

	//逆向输出双向链表的元素
	for {
		if temp.pre == nil {
			break
		}
		nodes = append(nodes, *temp)
		temp = temp.pre
	}
	return
}

func main() {
	head := &Node{}
	head1 := Node{data: 1}
	appendNode(head, &head1)
	head2 := Node{data: 2}
	appendNode(head, &head2)
	fmt.Println("追加元素后----------")
	nodes := list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("逆向输出----------")
	nodes = list1(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("插入元素后----------")
	head3 := Node{data: 3}
	insertNode(head, &head3)

	head4 := Node{data: 4}
	insertNode(head, &head4)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("逆向输出----------")
	nodes = list1(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("删除元素后----------")
	deleteNode(head, 3)
	deleteNode(head, 5)
	deleteNode(head, 4)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("逆向输出----------")
	nodes = list1(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}
}
