/*
 * Author: yunyu2019
 * Date: 2019-12-16 13:39:51
 * Description:
 */
//defer在真正的return之前执行，如果预定义了返回值t，则defer对t的对t的修改会对t起作用，返回的也是t本身；而如果预定义返回值，t是完全局部变量，则预备return的是其值的拷贝，后面对这个局部变量的任何修改都在函数结束时作为局部变量被销毁了，事实上返回的是defer之前准备好的值拷贝；
package main

import "fmt"

func main() {
	println(DeferFunc1(1)) //4
	println(DeferFunc2(1)) //1
	println(DeferFunc3(1)) //3
}

func DeferFunc1(i int) (t int) {
	t = i

	defer func() {
		t += 3
	}()

	return t
}

func DeferFunc2(i int) int {
	t := i

	defer func() {
		t += 3
	}()
	fmt.Println("func2 ", t)
	return t
}

func DeferFunc3(i int) (t int) {

	defer func() {
		t += i
	}()

	return 2
}
