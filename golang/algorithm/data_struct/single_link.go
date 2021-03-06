//单向链表
package main

import (
	"fmt"
)

type Node struct {
	data int
	next *Node
}

//追加元素
func appendList(head *Node, n *Node) {
	temp := head
	for {
		if temp.next == nil {
			break
		}
		temp = temp.next
	}
	temp.next = n
}

//插入元素
func insertList(head *Node, n *Node) {
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
	temp.next = n
}

//删除元素
func deleteList(head *Node, n int) {
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
}

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

/*
* getMiddle 获取单链表中间节点
* 思路:
* 初始化:定义两个指针分别指向单链表头节点,比如search指针和mid指针
* 运行中:search每次移动两次指针，mid每次移动一次指针，
* 结束条件:当search移动到最后节点后，mid的位置就是中间节点的位置
 */
func getMiddle(head *Node) *Node {
	if head.next == nil {
		return &Node{}
	}
	search := head
	mid := head
	for {
		if search.next == nil {
			break
		}
		if search.next.next != nil {
			search = search.next.next
		} else {
			search = search.next
		}
		mid = mid.next
	}
	return mid
}

func main() {
	head := &Node{}
	head1 := Node{data: 1}
	appendList(head, &head1)
	head2 := Node{data: 2}
	appendList(head, &head2)
	fmt.Println("追加元素后----------")
	nodes := list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("插入元素后----------")
	head3 := Node{data: 3}
	insertList(head, &head3)

	head4 := Node{data: 4}
	insertList(head, &head4)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("删除元素后----------")
	deleteList(head, 3)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}

	fmt.Println("查找中间节点----------")
	mid := getMiddle(head)
	fmt.Printf("中间节点是:%d\n", mid.data)
}
