package wnet

import (
	"C"
	"context"

	"fmt"
	"net"

	zmq "github.com/go-zeromq/zmq4"
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
	ZmqFromPy     zmq.Socket
	ZmqToPy       zmq.Socket
	ZmqFromPyAddr string
	ZmqToPyAddr   string
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
func StartNetThread(zmqFromPyAddr *C.char, zmqToPyAddr *C.char, ip *C.char, port int)  {
	s := NewNetServer()
	s.ZmqFromPyAddr = C.GoString(zmqFromPyAddr)
	s.ZmqToPyAddr = C.GoString(zmqToPyAddr)
	s.IP = C.GoString(ip)
	s.Port = port
	s.Start()
}


func (s *NetServer) Start() {
	ctx,_ := context.WithCancel(context.Background())
	s.ZmqStart(ctx)
	s.TcpStart(ctx)
}


func (s *NetServer) ZmqStart(ctx context.Context) {
	s.ZmqFromPy = zmq.NewPull(ctx)
	s.ZmqFromPy.SetOption(zmq.OptionHWM, 0)
	fmt.Println(" start listen:", s.ZmqFromPyAddr)
	s.ZmqFromPy.Listen(s.ZmqFromPyAddr)
	fmt.Println("listen finish ")


	s.ZmqToPy = zmq.NewPush(ctx)
	s.ZmqToPy.SetOption(zmq.OptionHWM, 0)
	fmt.Println("start connect:", s.ZmqToPyAddr)
	s.ZmqToPy.Dial(s.ZmqToPyAddr)
	fmt.Println("connect finish:", s.ZmqToPyAddr)
}


func (s *NetServer) TcpStart(ctx context.Context) {
	go func() {
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
	}()
}

func (s *NetServer) Stop() {
	fmt.Println("[STOP] Zinx server , name ", s.Name)
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
