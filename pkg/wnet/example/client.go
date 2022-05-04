package main
import (
	"fmt"
	"io"
	"net"
	"time"
	"wnet/wnet"
)


func main() {

	conn, err := net.Dial("tcp", "127.0.0.1:60300")
	if err != nil {
		fmt.Println("client start err, exit!", err)
		return
	}

	for {
		//发封包message消息
		dp := wnet.NewMsgPack()
		msg, _ := dp.Pack(wnet.NewMessage(uint32(wnet.CmdPacket), 10, []byte("PlayerLoginRequest")))
		_, err := conn.Write(msg)
		if err != nil {
			fmt.Println("write error err ", err)
			return
		}
		headData := make([]byte, dp.GetHeadLen())
		if _, err := io.ReadFull(conn, headData); err != nil {
			fmt.Println("read msg head error ", err)
			return
		}
		rcvMsg, err := dp.Unpack(headData)
		if err != nil {
			fmt.Println("unpack error ", err)
			return
		}
		var data []byte
		if rcvMsg.GetDataLen() > 0 {
			data = make([]byte, rcvMsg.GetDataLen())
			if _, err := io.ReadFull(conn, data); err != nil {
				fmt.Println("read msg data error ", err)
				return
			}
		}
		fmt.Println("recv ",string(data))
		time.Sleep(1 * time.Second)
	}
}

