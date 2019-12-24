/*
 * Author: yunyu2019
 * Date: 2019-12-24 11:13:50
 * Description:
 */
/*
* 判断单向链表是否有环
* 第一种方法:初始时两个指针都指向单向链表头结点,即初始化成单向链表头指针，假设指针为a和b,a指针总是一直向前走，b每次从头开始走，经过的结点都记录走的总步数,如果某个时刻经过一个节点时,指针a走过的步数不等于b指针走过的总步数，则存在环，参考文档:https://cloud.tencent.com/developer/article/1339608
* 第二种方法:使用快慢指针，初始时两个指针都指向单向链表头结点,即初始化成单向链表头指针，假设指针为a和b,a指针每次向前走两步，b指针每次向前走一步，如果某个时刻存在a和b指针相等了，则存在环。参考文档:https://www.cnblogs.com/newcaoguo/p/9384621.html
 */
package main

import "fmt"

//Node 结点结构体
type Node struct {
	Data int
	Next *Node
}

// checkCircle1 步数比较发
func checkCircle1(head *Node) bool {
	flag := false
	if head.Next == nil {
		return flag
	}
	var stePA, stepB int
	A := head
	var B *Node
Loop:
	for {
		if A.Next == nil {
			break
		}
		A = A.Next
		stePA++
		B = head
		stepB = 0
		for {
			if B.Next == nil {
				break
			}
			B = B.Next
			stepB++
			if B == A {
				fmt.Println(stePA, stepB)
				if stepB != stePA {
					fmt.Println(B)
					flag = true
					break Loop
				} else {
					break
				}
			}
		}
	}
	return flag
}

// checkCircle2 快慢指针检测
func checkCircle2(head *Node) bool {
	flag := false
	if head.Next == nil {
		return flag
	}
	fast := head
	slow := head
	for {
		if fast.Next == nil || slow.Next == nil {
			break
		}

		if fast.Next.Next != nil {
			fast = fast.Next.Next
		} else {
			fast = fast.Next
		}

		slow = slow.Next
		if fast == slow {
			flag = true
			break
		}
	}
	return flag
}

func main() {
	head := &Node{}
	node1 := &Node{Data: 1}
	node2 := &Node{Data: 2}
	node3 := &Node{Data: 3}
	node4 := &Node{Data: 4}
	node5 := &Node{Data: 5}
	node6 := &Node{Data: 6}
	head.Next = node1
	node1.Next = node2
	node2.Next = node3
	node3.Next = node4
	node4.Next = node5
	node5.Next = node6
	node6.Next = node3
	//flag := checkCircle2(head)
	flag := checkCircle1(head)
	if flag {
		fmt.Println("存在环")
	} else {
		fmt.Println("不存在环")
	}
}
