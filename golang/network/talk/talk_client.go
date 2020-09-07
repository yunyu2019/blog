//聊天室客户端
package main
import(
    "fmt"
    "net"
    "os"
)

func main() {
    conn,err := net.Dial("tcp","127.0.0.1:8004")
    if err != nil {
        fmt.Println("链接服务器监错误:",err)
        return
    }
    defer conn.Close()
    go func() {
        buf := make([]byte,4096)
        for {
            n,err := os.Stdin.Read(buf)
            if err != nil {
                fmt.Println("os.Stdin.Read err:",err)
                continue
            }
            conn.Write(buf[:n])
        }
    }()
    read_buf := make([]byte,4096)
    for {
        n,err := conn.Read(read_buf)
        if n == 0 {
            fmt.Println("终端连接已断开")
            return
        }
        if err != nil {
            fmt.Println("Read from server err:",err)
            return
        }
        fmt.Println(string(read_buf[:n]))
    }
}