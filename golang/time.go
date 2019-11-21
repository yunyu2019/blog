//周期性定时
package main
import (
    "time"
    "fmt"
)

func main() {
    quit := make(chan bool)
    myTimer := time.NewTicker(5*time.Second)
    i := 0
    go func() {
        for {
            now := <-myTimer.C
            fmt.Println(now)
            i++
            if i == 8 {
                quit <- true
                break
            }
        }
    }()
    <-quit
}