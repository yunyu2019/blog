package main
import (
"fmt"
"sync"
"time"
)

var mutex sync.Mutex

func Printer(s string) {
    mutex.Lock()
    for _,l := range s {
        fmt.Printf("%c",l)
        time.Sleep(time.Second)
    }
    mutex.Unlock()
}

func person1() {
    Printer("hello");
}

func person2() {
    Printer("world");
}

func main() {
    go person1()
    go person2()
    for {
        
    }
}