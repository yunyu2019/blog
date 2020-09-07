//读写锁
package main
import (
    "fmt"
    "sync"
    "time"
    "math/rand"
)

var mutex sync.RWMutex
var val int

func read(i int) {
    for {
        mutex.RLock()
        num := val
        fmt.Printf("%dth read num:%d\n",i,num)
        mutex.RUnlock()
    }
}

func write(i int) {
    for {
        num := rand.Intn(1000)
        mutex.Lock()
        val = num
        fmt.Printf("%dth write num:%d\n",i,num)
        time.Sleep(time.Millisecond * 300)
        mutex.Unlock()
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    for i := 0; i < 5; i++ {
        go read(i+1)
    }

    for i := 0; i < 5; i++ {
        go write(i+1)
    }

    for {
        
    }
}