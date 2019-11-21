//并发协程tcp socket服务器
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
    for {
        conn,err := socket.Accept()
        if err != nil {
            fmt.Println("服务器链接失败:",err)
            return
        }
        go func() {
            defer conn.Close()
            addr := conn.RemoteAddr()
            fmt.Printf("%s 与服务器建立连接成功\n",addr)
            buf := make([]byte,4096)
            for {
                n,err := conn.Read(buf)
                if "exit\n" == string(buf[:n]) || "exit\r\n" == string(buf[:n]) {
                    fmt.Println("接收终端关闭命令,断开终端连接")
                    return
                }
                if n == 0 {
                    fmt.Println("终端已关闭,断开连接")
                    return
                }

                if err != nil {
                    fmt.Println("信息读取失败:",err)
                    return
                }
                fmt.Println("服务器收到信息:",string(buf[:n]))
                conn.Write(buf[:n])
            }
        }()
    }
}