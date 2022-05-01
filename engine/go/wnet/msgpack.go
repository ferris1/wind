package wnet

import (
	"bytes"
	"encoding/binary"
	"errors"
)

type IMsgPack interface {
	GetHeadLen() uint32
	Pack(msg IMessage) ([]byte, error)
	Unpack([]byte) (IMessage, error)
}


var defaultHeaderLen uint32 = 8

type MsgPack struct{}

func NewMsgPack() IMsgPack {
	return &MsgPack{}
}

func (dp *MsgPack) GetHeadLen() uint32 {
	return defaultHeaderLen
}

func (dp *MsgPack) Pack(msg IMessage) ([]byte, error) {
	dataBuff := bytes.NewBuffer([]byte{})

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetDataLen()); err != nil {
		return nil, err
	}

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetMsgID()); err != nil {
		return nil, err
	}

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetData()); err != nil {
		return nil, err
	}

	return dataBuff.Bytes(), nil
}

func (dp *MsgPack) Unpack(binaryData []byte) (IMessage, error) {
	dataBuff := bytes.NewReader(binaryData)
	msg := &Message{}

	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.DataLen); err != nil {
		return nil, err
	}

	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.ID); err != nil {
		return nil, err
	}

	if msg.DataLen > MaxPacketSize {
		return nil, errors.New("too large msg data received")
	}

	return msg, nil
}
