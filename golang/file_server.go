//文件服务器 - 文件服务器(接收)端
package main
import (
    "fmt"
    "net"
    "os"
)

func main() {
    socket,err := net.Listen("tcp","127.0.0.1:8003")
    if err != nil {
        fmt.Println("服务器监听地址错误:",err)
        return
    }
    defer socket.Close()
    fmt.Println("服务器等待终端建立连接")
    conn,err := socket.Accept()
    if err != nil {
        fmt.Println("服务器链接失败:",err)
        return
    }
    defer conn.Close()
    fmt.Println("与服务器建立连接成功")
    buf := make([]byte,4096)
    n,err := conn.Read(buf)
    if err != nil {
        fmt.Println("服务器链接失败:",err)
        return
    }
    conn.Write([]byte("ok"))
    file_name := string(buf[:n])
    ch := make(chan bool)
    go func() {
        f,err := os.Create(file_name)
        if err != nil {
            fmt.Println("创建文件失败:",err)
            ch <- false
            return
        }

        defer f.Close()
        buf := make([]byte,4096)
        for { 
            n,err := conn.Read(buf)
            if n == 0 {
                fmt.Println("文件数据写入完毕")
                ch <- true
                return
            }
            if err != nil {
                fmt.Println("文件数据读取失败:",err)
                ch <- false
                return
            }
            f.Write(buf[:n])
        }
    }()
    <-ch
}