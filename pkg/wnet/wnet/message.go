package wnet

type IMessage interface {
	GetDataLen() uint32
	GetMsgID() uint32
	GetData() []byte
	GetCmdID() uint32
	GetPeerID() uint32

	SetMsgID(uint32)
	SetData([]byte)
	SetDataLen(uint32)
}

type Message struct {
	DataLen uint32
	MsgID   uint32
	Data    []byte
	CmdId   uint32
	PeerId  uint32
}

func NewMessage(cmdId uint32,ID uint32, data []byte) IMessage {
	return &Message{
		DataLen: uint32(len(data)),
		MsgID:   ID,
		Data:    data,
		CmdId:   cmdId,
	}
}

func NewPyMessage(CmdId uint32,PeerId uint32,ID uint32, data []byte) IMessage {
	return &Message{
		DataLen: uint32(len(data)),
		MsgID:   ID,
		CmdId:   CmdId,
		Data:    data,
		PeerId: PeerId,
	}
}

func (msg *Message) GetDataLen() uint32 {
	return msg.DataLen
}

func (msg *Message) GetMsgID() uint32 {
	return msg.MsgID
}

func (msg *Message) GetCmdID() uint32 {
	return msg.CmdId
}

func (msg *Message) GetPeerID() uint32 {
	return msg.PeerId
}

func (msg *Message) GetData() []byte {
	return msg.Data
}

func (msg *Message) SetDataLen(len uint32) {
	msg.DataLen = len
}

func (msg *Message) SetMsgID(msgID uint32) {
	msg.MsgID = msgID
}

func (msg *Message) SetData(data []byte) {
	msg.Data = data
}

func (msg *Message) SetCmdID(CmdId uint32) {
	msg.CmdId = CmdId
}

func (msg *Message) SetPeerID(peerId uint32) {
	msg.PeerId = peerId
}


