package main
import(
    "fmt"
)

func fb(ch <-chan int,quit <-chan bool) {
    for {
        select {
            case num := <-ch:
                fmt.Println(num)
            case <-quit:
                return
        }
    }
}

func main() {
    ch := make(chan int)
    quit := make(chan bool)
    go fb(ch,quit)
    x,y := 1,1
    for i := 0; i < 40; i++ {
        ch <- x
        x,y = y,x+y
    }
    quit <- true
}