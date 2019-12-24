/*
 * Author: yunyu2019
 * Date: 2019-12-24 14:37:00
 * Description:
 */

/*
* 问题描述:魔术师手中有A、2、3……J、Q、K十三张黑桃扑克牌。在表演魔术前，魔术师已经将他们按照一定的顺序叠放好（有花色的一面朝下）。魔术表演过程为：一开始，魔术师数1，然后把最上面的那张牌翻过来，是黑桃A；然后将其放到桌面上；第二次,魔术师数1、2；将第一张牌放到这些牌的最下面，将第二张牌翻转过来，正好是黑桃2；第三次，魔术师数1、2、3；将第1、2张牌依次放到这些牌的最下面，将第三张牌翻过来正好是黑桃3；……直到将所有的牌都翻出来为止。问原来牌的顺序是如何的。
* 算法方案:使用单向环形链表进行处理
 */
package main

import "fmt"

//Node 结点结构
type Node struct {
	data string
	next *Node
}

var cards map[int]string = map[int]string{
	1:  "A",
	2:  "2",
	3:  "3",
	4:  "4",
	5:  "5",
	6:  "6",
	7:  "7",
	8:  "8",
	9:  "9",
	10: "10",
	11: "J",
	12: "Q",
	13: "K",
}

var cardNum int = 13

//InitLinkList 初始化13个结点的链表
func InitLinkList() *Node {
	head := &Node{}
	curr := head
	for i := 1; i <= cardNum; i++ {
		node := &Node{data: "0"}
		if i == 1 {
			head = node
			curr = node
			curr.next = head
		} else {
			curr.next = node
			curr = node
			curr.next = head
		}
	}
	return head
}

//ShowList 遍历单链表
func ShowList(head *Node) (nodes []*Node) {
	if head == nil {
		return
	}
	curr := head
	for {
		nodes = append(nodes, curr)
		if curr.next == head {
			break
		}
		curr = curr.next
	}
	return
}

//dealCard 魔术师发方法
func dealCard(head *Node, cards map[int]string) *Node {
	curr := head
	curr.data = cards[1]
	var i int
	num := 2
	for {
		if num > cardNum {
			break
		}
		i = 1
		for {
			if i > num {
				break
			}
			curr = curr.next
			if curr.data == "0" {
				//只有未填充真实数字的纸牌才能计数
				i++
			}
		}
		curr.data = cards[num]
		num++
	}
	return head
}

func main() {
	head := InitLinkList()
	nodes := ShowList(head)
	fmt.Println("初始化纸牌-----------")
	for _, v := range nodes {
		fmt.Print(v.data, " ")
	}
	fmt.Println()

	fmt.Println("发放棋牌以后的结果--------")
	head = dealCard(head, cards)
	nodes = ShowList(head)
	for _, v := range nodes {
		fmt.Print(v.data, " ")
	}
	fmt.Println()
}
