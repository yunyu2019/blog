//冒泡排序
package main

import (
    "fmt"
)

func main() {
    a := [7]int{2,5,4,6,9,7,1}
    fmt.Println(a)
    for i,len := 0,len(a); i < len; i++ {
        for j := i+1; j < len; j++ {
            if a[i] < a[j] {
                a[i],a[j] = a[j],a[i]
            }
        }
    }
    fmt.Println(a)
}