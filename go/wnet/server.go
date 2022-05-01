package wnet

import (
	"fmt"
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
	Name       string
	IP         string
	Port       int
	IPVersion  string
	MsgHandler IMsgHandle
	ConnMgr    IConnManager
	Pack       IMsgPack
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

func (s *NetServer) Start() {
	fmt.Printf("[START] Server name: %s,listenner at IP: %s, Port %d is starting\n", s.Name, s.IP, s.Port)

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