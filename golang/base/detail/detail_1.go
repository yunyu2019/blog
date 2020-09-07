/*
 * @Author: yunyu2019
 * @Description:
 * @Date: 2019-12-13 10:09:32
 */

package main

import "fmt"

type Integer int

func (a Integer) Add(b Integer) Integer {
	return a + b
}

func (a *Integer) Add1(b Integer) Integer {
	return *a + b
}

func main() {
	var a Integer = 1
	var b Integer = 2
	var i interface{} = &a
	sum := i.(*Integer).Add(b)
	sum1 := i.(*Integer).Add1(b)
	fmt.Println(sum)  //正确
	fmt.Println(sum1) //正确
	/*
		var i interface{} = a
		sum := i.(Integer).Add(b)  //正确
		sum := i.(Integer).Add1(b) //错误

		fmt.Println(sum)
		fmt.Println(sum1)
	*/
	//总结:不涉及类型断言时，值和指针都可以调用【值方法】和【指针方法】
	//涉及类型断言时，值只能调用【值方法】，指针都可以调用
}
