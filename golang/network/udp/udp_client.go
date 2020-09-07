//udp客户端socket
package main
import (
    "fmt"
    "net"
)

func main() {
    conn,err := net.Dial("udp","127.0.0.1:8002")
    if err != nil {
        fmt.Println("链接服务器监错误:",err)
        return
    }
    defer conn.Close()
    conn.Write([]byte("ping"))
    buf := make([]byte,4096)
    n,err := conn.Read(buf)
    if err != nil {
        fmt.Println("信息读取失败:",err)
        return
    }
    fmt.Println("收到服务器信息:",string(buf[:n]))
}

