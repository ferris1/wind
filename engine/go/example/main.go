package main
import (
	"fmt"
	"net"
	"time"
	"wind/wnet"
)


func main() {

	conn, err := net.Dial("tcp", "127.0.0.1:60000")
	if err != nil {
		fmt.Println("client start err, exit!", err)
		return
	}

	for {
		//发封包message消息
		dp := wnet.NewMsgPack()
		msg, _ := dp.Pack(wnet.NewMessage(0, []byte("Zinx client Demo Test MsgID=0, [Ping]")))
		_, err := conn.Write(msg)
		if err != nil {
			fmt.Println("write error err ", err)
			return
		}
		time.Sleep(1 * time.Second)
	}
}

