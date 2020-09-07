//udp服务器socket
package main
import (
    "fmt"
    "net"
)

func main() {
    udp_addr,err := net.ResolveUDPAddr("udp","127.0.0.1:8002")
    if err != nil {
        fmt.Println("创建udp服务器监听地址错误:",err)
        return
    }
    fmt.Println("创建udp服务器监听地址成功")
    conn,err := net.ListenUDP("udp",udp_addr)
    if err != nil {
        fmt.Println("创建udp服务器通信socket错误:",err)
        return
    }
    fmt.Println("创建udp服务器通信socket成功")
    defer conn.Close()
    buf := make([]byte,4096)
    n,client_addr,err := conn.ReadFromUDP(buf)
    if err != nil {
        fmt.Println("udp服务器读取信息错误:",err)
        return
    }
    fmt.Printf("udp服务器读取来自 %v 的信息: %s\n",client_addr,string(buf[:n]))
    _,err = conn.WriteToUDP(buf[:n],client_addr)
    if err != nil {
        fmt.Println("udp服务器读取信息错误:",err)
        return
    }
}