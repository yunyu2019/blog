//聊天室服务端
package main
import(
    "fmt"
    "net"
    "strings"
    "time"
)

type Client struct {
    Name string
    Addr string
    Ch chan string
}

var clients map[string]Client
var message = make(chan string)

func WriteMsg(conn net.Conn,cln Client) {
    for msg := range cln.Ch {
        conn.Write([]byte(msg + "\n"))
    }
}

func Connect(conn net.Conn) {
    defer conn.Close()
    ch := make(chan string)
    addr := conn.RemoteAddr().String()
    cln := Client{addr,addr,ch}
    clients[addr] = cln
    go WriteMsg(conn,cln)
    message <- fmt.Sprintf("%s|%s 已上线",addr,cln.Name)
    buf := make([]byte,4096)
    isQuit := make(chan bool)
    isLive := make(chan bool)
    go func() {
        for {
            n,err := conn.Read(buf)
            if n == 0 {
                fmt.Printf("终端 addr:%s 已关闭\n",addr)
                isQuit <- true
                return
            }

            if err != nil {
                fmt.Println("信息读取失败:",err)
                return
            }

            msg := string(buf[:n])
            msg = strings.TrimRight(msg,"\n")
            msg = strings.TrimRight(msg,"\r")
            if msg == "who" || msg == "who" {
                //查询在线用户列表
                conn.Write([]byte("online users:\n"))
                for _,c := range clients {
                    user := c.Addr + "|" + c.Name + "\n"
                    conn.Write([]byte(user))
                }
            } else if len(msg) >8 && msg[:6] == "rename" {
                //修改终端用户名
                new_name := strings.Split(msg,"|")[1]
                cln.Name = new_name
                clients[addr] = cln
                conn.Write([]byte("修改name成功\n"))
            } else {
                message <- fmt.Sprintf("%s|%s msg:%s",addr,cln.Name,msg)
            }
            isLive <- true
        }
    }()

    for {
        select {
            case <-isQuit:
                //用户主动退出
                close(cln.Ch)
                delete(clients,addr)
                message <- fmt.Sprintf("%s|%s 已下线",addr,cln.Name)
                return
            case <-isLive:
                //活跃状态
            case <-time.After(time.Second * 300):
                //不活跃超时被动退出
                delete(clients,addr)
                message <- fmt.Sprintf("%s|%s 5分钟没活跃,已下线",addr,cln.Name)
                return
        }
    }
}

func Manager() {
    clients = make(map[string]Client)
    for {
        msg := <-message
        for _,c := range clients {
            c.Ch <- msg
        }
    }
}

func main() {
    socket,err := net.Listen("tcp","127.0.0.1:8004")
    if err != nil {
        fmt.Println("服务器监听地址错误:",err)
        return
    }
    defer socket.Close()
    fmt.Println("服务器等待终端建立连接")
    go Manager()
    for {
        conn,err := socket.Accept()
        if err != nil {
            fmt.Println("服务器链接失败:",err)
            return
        }
        go Connect(conn)
    }
}