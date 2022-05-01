package wnet

import (
	"bytes"
	"encoding/binary"
	"errors"
)

type IMsgPack interface {
	GetHeadLen() uint32                //获取包头长度方法
	Pack(msg IMessage) ([]byte, error) //封包方法
	Unpack([]byte) (IMessage, error)   //拆包方法
}


var defaultHeaderLen uint32 = 8

//DataPack 封包拆包类实例，暂时不需要成员
type MsgPack struct{}

//NewDataPack 封包拆包实例初始化方法
func NewMsgPack() IMsgPack {
	return &MsgPack{}
}

//GetHeadLen 获取包头长度方法
func (dp *MsgPack) GetHeadLen() uint32 {
	//ID uint32(4字节) +  DataLen uint32(4字节)
	return defaultHeaderLen
}

//Pack 封包方法(压缩数据)
func (dp *MsgPack) Pack(msg IMessage) ([]byte, error) {
	//创建一个存放bytes字节的缓冲
	dataBuff := bytes.NewBuffer([]byte{})

	//写dataLen
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetDataLen()); err != nil {
		return nil, err
	}

	//写msgID
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetMsgID()); err != nil {
		return nil, err
	}

	//写data数据
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetData()); err != nil {
		return nil, err
	}

	return dataBuff.Bytes(), nil
}

//Unpack 拆包方法(解压数据)
func (dp *MsgPack) Unpack(binaryData []byte) (IMessage, error) {
	//创建一个从输入二进制数据的ioReader
	dataBuff := bytes.NewReader(binaryData)

	//只解压head的信息，得到dataLen和msgID
	msg := &Message{}

	//读dataLen
	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.DataLen); err != nil {
		return nil, err
	}

	//读msgID
	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.ID); err != nil {
		return nil, err
	}

	//判断dataLen的长度是否超出我们允许的最大包长度
	if msg.DataLen > MaxPacketSize {
		return nil, errors.New("too large msg data received")
	}

	//这里只需要把head的数据拆包出来就可以了，然后再通过head的长度，再从conn读取一次数据
	return msg, nil
}
