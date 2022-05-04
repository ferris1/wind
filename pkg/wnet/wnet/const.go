package wnet

type ServerCmdEnum int

const (
	CmdNone   			ServerCmdEnum =  0
	CmdInit				ServerCmdEnum =  1
	CmdConnect  		ServerCmdEnum =  2
	CmdDisconnect  		ServerCmdEnum =  3
	CmdPacket			ServerCmdEnum =  4


	CmdSend				ServerCmdEnum =  100
	CmdExit 			ServerCmdEnum =  101
)

var (
	MaxConn int32 = 50000
	MaxPacketSize uint32 = 1024*1024*2
	MaxWorkerTaskLen int32 = 1000
	PeerIDStart      uint32 = 1000
	PyConnId         uint32 = 10
	DDMMYYYYhhmmss = "2006-01-02 15:04:05,972"
)
