//文件服务器 - 文件发送(客户)端
package main
import (
    "fmt"
    "net"
    "os"
    "io"
)

func sendFile(conn net.Conn,file_path string) {
    f,err := os.Open(file_path)
    if err != nil {
        fmt.Println("读书文件失败,",err)
        return
    }

    buf := make([]byte,4096)
    for {
        n,err := f.Read(buf)
        if err != nil {
            if err == io.EOF {
                fmt.Println("文件读取完毕")
            } else {
                fmt.Println("读取文件信息失败,",err)
            }
            return
        }

        _,err = conn.Write(buf[:n])
        if err != nil {
            fmt.Println("向文件服务器发送文件数据错误:",err)
            return
        }
    }
}

func main() {
    list := os.Args
    if len(list) != 2 {
        fmt.Println("参数缺失")
        return
    }
    file_path := list[1]
    file_info,err := os.Stat(file_path)
    if err != nil {
        if os.IsExist(err) == false {
            fmt.Println("源文件不存在")
        } else {
            fmt.Println("获取文件信息错误")
        }
        return
    }

    file_name := file_info.Name()
    conn,err := net.Dial("tcp","127.0.0.1:8003")
    if err != nil {
        fmt.Println("与文件服务器连接失败,",err)
        return
    }
    defer conn.Close()
    _,err = conn.Write([]byte(file_name))
    if err != nil {
        fmt.Println("向文件服务器发送信息错误:",err)
        return
    }

    buf := make([]byte,4096)
    n,err := conn.Read(buf)
    if err != nil {
        fmt.Println("从文件服务器读取信息错误:",err)
        return
    }
    fmt.Println("从文件服务器读取信息:",string(buf[:n]))
    if string(buf[:n]) == "ok" {
        sendFile(conn,file_path)
    }
}