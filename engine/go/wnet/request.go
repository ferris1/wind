package wnet


type IRequest interface {
	GetConnection() 	IConnection
	GetData() 			[]byte
	GetMsgID() 			uint32
}

type Request struct {
	conn IConnection
	msg  IMessage
}

func (r *Request) GetConnection() IConnection {
	return r.conn
}

func (r *Request) GetData() []byte {
	return r.msg.GetData()
}

func (r *Request) GetMsgID() uint32 {
	return r.msg.GetMsgID()
}

