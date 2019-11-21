//tcp服务器socket
package main
import(
    "fmt"
    "net"
)

func main() {
    socket,err := net.Listen("tcp","127.0.0.1:8000")
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
        fmt.Println("信息读取失败:",err)
        return
    }
    fmt.Println("服务器收到信息:",string(buf[:n]))
    conn.Write([]byte("pong"))
}