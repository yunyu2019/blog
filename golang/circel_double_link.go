//环形单向链表
package main

import (
	"fmt"
)

type Node struct {
	data int
	next *Node
}

func appendNode(head *Node, n *Node) {
	if head.next == nil {
		head.data = n.data
		head.next = head
		return
	}
	temp := head
	for {
		if temp.next == head {
			break
		}
		temp = temp.next
	}
	temp.next = n
	n.next = head
}

/**
初始化temp:指向环形首部元素
初始化helper：指向环形末尾元素
*/
func deleteNode(head *Node, n int) *Node {
	temp := head
	if temp.next == nil {
		//空链表
		return head
	}

	//只有一个结点
	if temp.next == head {
		if temp.data == n {
			temp.next = nil
		}
		return head
	}

	//helper初始化为环形链表的最后一个元素
	helper := head
	for {
		if helper.next == head {
			break
		}
		helper = helper.next
	}

	flag := true
	for {
		if temp.next == head {
			break
		}
		if temp.data == n {
			//已找到元素
			if temp == head {
				//删除首个元素处理,移动首部指针
				head = head.next
			}
			helper.next = temp.next
			flag = false
			break
		}
		temp = temp.next
		helper = helper.next
	}

	if flag {
		if temp.data == n {
			helper.next = temp.next
		} else {
			fmt.Println("节点数据不存在")
		}
	}
	return head

}

func list(head *Node) (nodes []Node) {
	temp := head
	if temp.next == nil {
		return
	}
	for {
		nodes = append(nodes, *temp)
		if temp.next == head {
			break
		}
		temp = temp.next
	}
	return
}

func main() {
	head := &Node{}
	n := 30
	for i := 1; i <= n; i++ {
		head1 := &Node{data: i}
		appendNode(head, head1)
	}
	nodes := list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}
	fmt.Println("删除不存在的元素后----------")
	head = deleteNode(head, 31)
	fmt.Println("删除首元素后----------")
	head = deleteNode(head, 1)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}
	fmt.Println("删除末尾元素后----------")
	head = deleteNode(head, 30)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}
	fmt.Println("删除中间元素后----------")
	head = deleteNode(head, 28)
	nodes = list(head)
	for _, v := range nodes {
		fmt.Println(v.data)
	}
}
