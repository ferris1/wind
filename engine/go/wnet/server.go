package wnet

import (
	"fmt"
	"net"
)

var (
	MaxConn int32 = 0
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
	}
	return s
}

//Start 开启网络服务
func (s *NetServer) Start() {
	fmt.Printf("[START] Server name: %s,listenner at IP: %s, Port %d is starting\n", s.Name, s.IP, s.Port)

	//开启一个go去做服务端Linster业务
	go func() {
		//0 启动worker工作池机制
		s.MsgHandler.StartWorkerPool()

		//1 获取一个TCP的Addr
		addr, err := net.ResolveTCPAddr(s.IPVersion, fmt.Sprintf("%s:%d", s.IP, s.Port))
		if err != nil {
			fmt.Println("resolve tcp addr err: ", err)
			return
		}

		//2 监听服务器地址
		listener, err := net.ListenTCP(s.IPVersion, addr)
		if err != nil {
			panic(err)
		}

		//已经监听成功
		fmt.Println("start Wnet server  ", s.Name, " succ, now listenning...")

		//TODO server.go 应该有一个自动生成ID的方法
		var cID uint32
		cID = 0

		//3 启动server网络连接业务
		for {
			//3.1 阻塞等待客户端建立连接请求
			conn, err := listener.AcceptTCP()
			if err != nil {
				fmt.Println("Accept err ", err)
				continue
			}
			fmt.Println("Get conn remote addr = ", conn.RemoteAddr().String())

			//3.2 设置服务器最大连接控制,如果超过最大连接，那么则关闭此新的连接
			if s.ConnMgr.Len() >= MaxConn {
				_ = conn.Close()
				continue
			}

			//3.3 处理该新连接请求的 业务 方法， 此时应该有 handler 和 conn是绑定的
			dealConn := NewConnection(s, conn, cID, s.MsgHandler)
			cID++

			//3.4 启动当前链接的处理业务
			go dealConn.Start()
		}
	}()
}

//Stop 停止服务
func (s *NetServer) Stop() {
	fmt.Println("[STOP] Zinx server , name ", s.Name)

	//将其他需要清理的连接信息或者其他信息 也要一并停止或者清理
	s.ConnMgr.ClearConn()
}

//Serve 运行服务
func (s *NetServer) Serve() {
	s.Start()

	//TODO Server.Serve() 是否在启动服务的时候 还要处理其他的事情呢 可以在这里添加

	//阻塞,否则主Go退出， listenner的go将会退出
	select {}
}

//Serve 运行服务
func (s *NetServer) Packet() IMsgPack {
	return s.Pack
}

//Serve 运行服务
func (s *NetServer) GetConnMgr() IConnManager {
	return s.ConnMgr
}