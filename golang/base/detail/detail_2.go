/*
 * Author: yunyu2019
 * Date: 2019-12-13 11:11:52
 * Description:
 */

package main

import "fmt"

type Persion interface {
	getName() string
}

type Student struct {
	Name string
}

func (s *Student) getName() string {
	return s.Name
}

func main() {
	var p Persion = &Student{"lala"}
	name := p.getName() //正确
	fmt.Println(name)

	/*
		var p Persion = Student{"lala"}
		name := p.getName()//错误
		fmt.Println(name)
	*/
	//使用指针实现的接口，只能用指针去赋值接口；使用值实现的接口，指针和值都可以赋值接口；
}
