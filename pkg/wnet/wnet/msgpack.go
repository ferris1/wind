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

	GetPyHeadLen() uint32
	PackPy(msg IMessage) ([]byte, error)
	UnpackPy([]byte) (IMessage, error)
}


var defaultHeaderLen uint32 = 8
var defaultPyHeaderLen uint32 = 12

type MsgPack struct{}

func NewMsgPack() IMsgPack {
	return &MsgPack{}
}

func (dp *MsgPack) GetHeadLen() uint32 {
	return defaultHeaderLen
}

// peer_id,ctrl, dataLen
func (dp *MsgPack) GetPyHeadLen() uint32 {
	return defaultPyHeaderLen
}


func (dp *MsgPack) Pack(msg IMessage) ([]byte, error) {
	dataBuff := bytes.NewBuffer([]byte{})

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetMsgID()); err != nil {
		return nil, err
	}
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetDataLen()); err != nil {
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

	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.ID); err != nil {
		return nil, err
	}
	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.DataLen); err != nil {
		return nil, err
	}

	if msg.DataLen > MaxPacketSize {
		return nil, errors.New("too large msg data received")
	}

	return msg, nil
}

func (dp *MsgPack) PackPy(msg IMessage) ([]byte, error) {
	dataBuff := bytes.NewBuffer([]byte{})

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetCmdID()); err != nil {
		return nil, err
	}

	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetMsgID()); err != nil {
		return nil, err
	}
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetDataLen()); err != nil {
		return nil, err
	}
	if err := binary.Write(dataBuff, binary.LittleEndian, msg.GetData()); err != nil {
		return nil, err
	}

	return dataBuff.Bytes(), nil
}

func (dp *MsgPack) UnpackPy(binaryData []byte) (IMessage, error) {
	dataBuff := bytes.NewReader(binaryData)
	msg := &Message{}

	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.CmdId); err != nil {
		return nil, err
	}
	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.ID); err != nil {
		return nil, err
	}
	if err := binary.Read(dataBuff, binary.LittleEndian, &msg.DataLen); err != nil {
		return nil, err
	}

	if msg.DataLen > MaxPacketSize {
		return nil, errors.New("too large msg data received")
	}

	return msg, nil
}
