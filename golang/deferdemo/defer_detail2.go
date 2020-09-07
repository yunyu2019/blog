/*
 * Author: yunyu2019
 * Date: 2019-12-16 10:30:53
 * Description:
 */
//解析：注意defer所引导的如果不是匿名函数而是一个API调用，那么它会事先准备好所有参数（此时a,b的值还没有发生改变），并等待延时执行；而如果defer引导的是一个匿名函数时，那么函数体内部的代码则不会事先“预做准备”，而是到执行时才去读取a,b的具体值；
package main

import "fmt"

func calc(index string, a, b int) int {
	ret := a + b
	fmt.Println(index, a, b, ret)
	return ret
}

func main061() {
	a := 1
	b := 2

	defer calc("1", a, calc("10", a, b)) //A 这里a、b传入的是1和2

	a = 0
	defer calc("2", a, calc("20", a, b)) //B 这里a、b传入的还是0和2
	b = 1
	/*
		* defer执行函数，传入函数的值在定义defer的位置已经传入,所以A位置传入的是1和2，B位置传入的是0和2
			10 1 2 3
			20 0 2 2
			2 0 2 2
			1 1 3 4
	*/
}

func main() {
	main061()
	fmt.Println("-------------------------")
	main062()
}

func main062() {
	a := 1
	b := 2

	defer func() {
		calc("1", a, calc("10", a, b))
	}()

	a = 0

	defer func() {
		calc("2", a, calc("20", a, b))
	}()

	b = 1
	/*
		* 整个过程放入defer匿名函数中,a和b的结果都已更改为0和1
			20 0 1 1
			2 0 1 1
			10 0 1 1
			1 0 1 1
	*/
}
