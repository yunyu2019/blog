//条件变量控制互斥锁hong(协程共享数据)
package main
import(
    "fmt"
    "sync"
    "time"
    "math/rand"
)

var cond sync.Cond
func consumer(ch <-chan int,i int) {
    for {
        cond.L.Lock()
        for l := len(ch);l == 0; {
            cond.Wait()
        }
        num := <-ch
        fmt.Printf("%dth read num:%d\n",i,num)
        cond.L.Unlock()
        cond.Signal()
    }
}

func product(ch chan<- int,i int) {
    for {
        num := rand.Intn(1000)
        cond.L.Lock()
        for l,c := len(ch),cap(ch);l == c; {
            cond.Wait()
        }
        ch<-num
        fmt.Printf("%dth write num:%d\n",i,num)
        cond.L.Unlock()
        cond.Signal()
        time.Sleep(time.Millisecond * 300)
    }
}

func main() {
    rand.Seed(time.Now().UnixNano())
    ch := make(chan int,3)
    cond.L = new(sync.Mutex)
    for i := 0; i < 5; i++ {
        go product(ch,i+1)
    }

    for i := 0; i < 3; i++ {
        go consumer(ch,i+1)
    }
    for{

    }
}