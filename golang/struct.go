package main
import (
    "fmt"
)

type Persion struct{
    Name string
    Age int
    Loves []string
}

func Modify(p *Persion) {
    p.Name = "xiaohua"
    p.Age = 6
    p.Loves = append(p.Loves,"pingpang")
    p.Loves = append(p.Loves,"music")
}

func main() {
    p := Persion{"xiaoxiao",10,[]string{"movie","history"}}
    fmt.Println(p)
    Modify(&p)
    fmt.Println(p)
}