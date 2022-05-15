package wnet

import (
	"net"
	"strconv"
)

type IMsgHandle interface {
	DoMsgHandler(request IRequest)
	StartNetWorker()
	SendMsgToTaskQueue(request IRequest)
	SetServer(server INetServer)
}

type MsgHandle struct {
	TaskQueue      		chan IRequest
	Server      		INetServer
}

func NewMsgHandle() *MsgHandle {
	return &MsgHandle{
		TaskQueue: make(chan IRequest, MaxWorkerTaskLen),
	}
}

func (mh *MsgHandle) SetServer(server INetServer) {
	mh.Server = server
}

func (mh *MsgHandle) SendMsgToTaskQueue(request IRequest) {
	mh.TaskQueue <- request
}

// 这里应该开两个线程  一个处理客户端数据  一个处理Python端数据
func (mh *MsgHandle) StartNetWorker()  {
	for {
		select {
		case request := <-mh.TaskQueue:
			if request.GetConnection().GetIsPyConn() {
				mh.DoPyMsgHandler(request)
			} else {
				mh.DoMsgHandler(request)
			}
		}
	}
}
//处理客户端的数据
func (mh *MsgHandle) DoMsgHandler(request IRequest) {
	pyConn,err := mh.Server.GetConnMgr().Get(PyConnId)
	if err != nil {
		NetLog.Erorr("no py conn")
		return
	}
	conn := request.GetConnection()
	switch ServerCmdEnum(request.GetCmdID()) {
	case CmdConnect:
		ip, port, err := net.SplitHostPort(conn.RemoteAddr().String())
		if err!=nil {
			break
		}
		intPort,err := strconv.Atoi(port)
		_ = pyConn.SendPyMsg(uint32(CmdConnect), conn.GetPeerID(), uint32(intPort), []byte(ip))
		break
	case CmdDisconnect:
		_ = pyConn.SendPyMsg(uint32(CmdDisconnect), conn.GetPeerID(), request.GetMsgID(), request.GetData())
		break
	default: // 默认直接发给python端
		_ = pyConn.SendPyMsg(uint32(CmdPacket), conn.GetPeerID(), request.GetMsgID(), request.GetData())
		break
	}
}

//处理Python端的数据
func (mh *MsgHandle) DoPyMsgHandler(request IRequest) {
	//pyConn := request.GetConnection()
	switch ServerCmdEnum(request.GetCmdID()) {
	case CmdExit:
		mh.Server.Stop()
		break
	case CmdDisconnect:
		conn,err := mh.Server.GetConnMgr().Get(request.GetPeerID())
		if err == nil {
			conn.Stop()
		}
		break
	case CmdSend:
		conn,err := mh.Server.GetConnMgr().Get(request.GetPeerID())
		if err == nil {
			_ = conn.SendMsg(request.GetMsgID(), request.GetData())
		}
	default:
		NetLog.Erorr("no py cmd")
	}
}

