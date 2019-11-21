package main
import (
    "fmt"
)

func main() {
    A()
    B()
    C()
}

func A() {
    fmt.Println("A")
}

func B() {
    defer func() {
        if err := recover();err != nil {
            fmt.Println("recover")
        }
    }()
    fmt.Println("B")
    panic("B panic")
    
}

func C() {
    fmt.Println("C")
}