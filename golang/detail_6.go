/*
 * Author: yunyu2019
 * Date: 2019-12-16 10:28:07
 * Description:
 */
package main

import "fmt"

type People struct{}

func (p *People) ShowA() {
	fmt.Println("showA")
	p.ShowB()
}
func (p *People) ShowB() {
	fmt.Println("showB")
}

type Teacher struct {
	People
}

func (t *Teacher) ShowB() {
	fmt.Println("teachershowB")
}

func main() {
	t := Teacher{}
	t.ShowA() //show方法中的指针指向的是people对象,则在ShowA()中调用的就是people对象的ShowB方法
	t.ShowB()
}
