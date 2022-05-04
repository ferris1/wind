package wnet

type ServerCmdEnum int

const (
	CmdNone   			ServerCmdEnum =  0
	CmdInit				ServerCmdEnum =  1
	CmdConnect  		ServerCmdEnum =  2
	CmdDisconnect  		ServerCmdEnum =  3
	CmdPacket			ServerCmdEnum =  4
)

