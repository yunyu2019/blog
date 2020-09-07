/*
* 约瑟夫问题
问题描述:一堆猴子都有编号，编号是1，2，3 ...m，这群猴子（m个）按照1-m的顺序围坐一圈，从第1开始数，每数到第N个，该猴子就要离开此圈，这样依次下来，直到圈中只剩下最后一只猴子，
则该猴子为大王。
*/
package main

import (
	"fmt"
)

type Node struct {
	data int
	next *Node
}

func getNodes(n int) *Node {
	head := &Node{}
	current := &Node{}
	for i := 1; i <= n; i++ {
		node := &Node{data: i}
		if i == 1 {
			head = node
			current = node
			current.next = head
		} else {
			current.next = node
			current = node
			current.next = head
		}
	}
	return head
}

func showNodes(head *Node) (nodes []Node) {
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

/*
start:从第start位置开始数
count:每次数几个数
*/
func Play(head *Node, start int, count int) (nums []int) {
	if head.next == nil {
		return
	}

	tail := head
	for {
		if tail.next == head {
			break
		}
		tail = tail.next
	}

	//head指针移动到start位置
	for i := 1; i <= start-1; i++ {
		head = head.next
		tail = tail.next
	}

	for {
		if tail == head {
			nums = append(nums, head.data)
			break
		}
		for j := 1; j <= count-1; j++ {
			head = head.next
			tail = tail.next
		}
		nums = append(nums, head.data)
		head = head.next
		tail.next = head
	}
	return
}

func main() {
	var n int = 50
	head := getNodes(n)
	nodes := showNodes(head)
	for _, m := range nodes {
		fmt.Println(m.data)
	}
	fmt.Println("开始出列游戏")
	nums := Play(head, 1, 4)
	for _, m := range nums {
		fmt.Println(m)
	}
}
