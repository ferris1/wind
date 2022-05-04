package wnet

import (
	"C"
	"fmt"
	"io"
	"net"
)

var (
	MaxConn int32 = 50000
	MaxPacketSize uint32 = 1024*1024*2
	WorkerPoolSize int32 = 1
	MaxWorkerTaskLen int32 = 10000
)

//定义服务接口
type INetServer interface {
	Start()
	Stop()
	Serve()
	Packet()  		IMsgPack
	GetConnMgr() 	IConnManager
}

type NetServer struct {
	Name          string
	IP            string
	Port          int
	IPVersion     string
	MsgHandler    IMsgHandle
	ConnMgr       IConnManager
	Pack          IMsgPack
	NetFromPyAddr string
	NetToPyAddr   string

	FromPyConn 			net.Conn
}

func NewNetServer() *NetServer {
	s := &NetServer{
		Name:       "NetServer",
		IP:         "127.0.0.1",
		Port:       60000,
		IPVersion:  "tcp4",
		MsgHandler: NewMsgHandle(),
		ConnMgr:    NewConnManager(),
		Pack: 		NewMsgPack(),
	}
	return s
}

//export StartNetThread
func StartNetThread(netFromPyAddr *C.char, netToPyAddr *C.char, ip *C.char, port int)  {
	s := NewNetServer()
	s.NetFromPyAddr = C.GoString(netFromPyAddr)
	s.NetToPyAddr = C.GoString(netToPyAddr)
	s.IP = C.GoString(ip)
	s.Port = port
	s.Start()
}

func (s *NetServer) Start() {
	go s.PyNetStart()
	go s.TcpStart()
}

func (s *NetServer) PyNetStart() {
	conn, err := net.Dial("tcp", "127.0.0.1:60010")
	if err != nil {
		fmt.Println("client start err, exit!", err)
		return
	}
	s.FromPyConn = conn
	for {
		//发封包message消息
		dp := NewMsgPack()
		msg, _ := dp.PackPy(NewPyMessage(0, uint32(CmdInit),[]byte("hello")))
		_, err = s.FromPyConn.Write(msg)
		if err != nil {
			fmt.Println("write error err ", err)
			continue
		}
		pymsg := s.ReadFromPy()
		if pymsg != nil && ServerCmdEnum(pymsg.GetCmdID()) == CmdInit {
			fmt.Println("PyNetStart finish")
			break
		}
	}
}

func (s *NetServer) ReadFromPy() IMessage {
	headData := make([]byte, s.Packet().GetPyHeadLen())
	if _, err := io.ReadFull(s.FromPyConn, headData); err != nil {
		fmt.Println("read msg head error ", err)
		return nil
	}
	msg, err := s.Packet().UnpackPy(headData)
	if err != nil {
		fmt.Println("unpack error ", err)
		return nil
	}
	var data []byte
	if msg.GetDataLen() > 0 {
		data = make([]byte, msg.GetDataLen())
		if _, err := io.ReadFull(s.FromPyConn, data); err != nil {
			fmt.Println("read msg data error ", err)
			return nil
		}
	}
	msg.SetData(data)
	return msg
}

func (s *NetServer) TcpStart() {
	s.MsgHandler.StartWorkerPool()
	addr, err := net.ResolveTCPAddr(s.IPVersion, fmt.Sprintf("%s:%d", s.IP, s.Port))
	if err != nil {
		fmt.Println("resolve tcp addr err: ", err)
		return
	}
	listener, err := net.ListenTCP(s.IPVersion, addr)
	if err != nil {
		panic(err)
	}
	fmt.Println("start Wnet server  ", s.Name, " succ, now listenning...")
	var cID uint32
	cID = 0
	for {
		conn, err := listener.AcceptTCP()
		if err != nil {
			fmt.Println("Accept err ", err)
			continue
		}
		fmt.Println("Get conn remote addr = ", conn.RemoteAddr().String())
		if s.ConnMgr.Len() >= MaxConn {
			_ = conn.Close()
			continue
		}
		dealConn := NewConnection(s, conn, cID, s.MsgHandler)
		cID++
		go dealConn.Start()
	}
}


func (s *NetServer) Stop() {
	fmt.Println("[STOP] Wnet server , name ", s.Name)
	s.ConnMgr.ClearConn()
}

func (s *NetServer) Serve() {
	s.Start()
	select {}
}

func (s *NetServer) Packet() IMsgPack {
	return s.Pack
}

func (s *NetServer) GetConnMgr() IConnManager {
	return s.ConnMgr
}
