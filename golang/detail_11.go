/*
 * Author: yunyu2019
 * Date: 2019-12-16 15:13:17
 * Description:
 */
//注意一个函数内部多次panic时，以最后一次为准；
package main

import (
	"fmt"
	"reflect"
)

func main301() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println(err) //
		} else {
			fmt.Println("fatal")
		}
	}()

	/*一个函数内多次panic以后发的为准*/
	defer func() {
		panic("defer panic")
	}()

	panic("你妹")
}

func main302() {
	defer func() {
		if err := recover(); err != nil {
			fmt.Println("++++")
			f := err.(func() string)

			fmt.Println(err, f(), reflect.TypeOf(err), reflect.TypeOf(err).Kind().String()) //地址，defer panic，func()string,func
		} else {
			fmt.Println("fatal")
		}
	}()

	defer func() {
		panic(func() string {
			return "defer panic"
		})
	}()

	panic("你妹")
}

func main() {
	main301() //defer panic
	fmt.Println("------------------")
	main302()
}
