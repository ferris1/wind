package wnet

type IMessage interface {
	GetDataLen() uint32
	GetMsgID() uint32
	GetData() []byte

	SetMsgID(uint32)
	SetData([]byte)
	SetDataLen(uint32)
}


type Message struct {
	DataLen uint32
	ID      uint32
	Data    []byte
}

func NewMessage(ID uint32, data []byte) IMessage {
	return &Message{
		DataLen: uint32(len(data)),
		ID:      ID,
		Data:    data,
	}
}

func (msg *Message) GetDataLen() uint32 {
	return msg.DataLen
}

func (msg *Message) GetMsgID() uint32 {
	return msg.ID
}

func (msg *Message) GetData() []byte {
	return msg.Data
}

func (msg *Message) SetDataLen(len uint32) {
	msg.DataLen = len
}

func (msg *Message) SetMsgID(msgID uint32) {
	msg.ID = msgID
}

func (msg *Message) SetData(data []byte) {
	msg.Data = data
}

