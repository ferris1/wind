package wnet

import (
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"sync"
	"time"
)


type IConnection interface {
	Start()
	Stop()
	Context() context.Context

	GetTCPConnection() *net.TCPConn
	GetConnID() uint32
	RemoteAddr() net.Addr

	SendMsg(msgID uint32, data []byte) error
	SendBuffMsg(msgID uint32, data []byte) error
}


type Connection struct {
	Server 			INetServer
	Conn 			*net.TCPConn
	ConnID 			uint32
	MsgHandler 		IMsgHandle
	ctx    context.Context
	cancel context.CancelFunc
	msgBuffChan chan []byte

	sync.RWMutex
	propertyLock sync.Mutex
	isClosed bool
}

func NewConnection(server INetServer, conn *net.TCPConn, connID uint32, msgHandler IMsgHandle) IConnection {
	//初始化Conn属性
	c := &Connection{
		Server:   	server,
		Conn:        conn,
		ConnID:      connID,
		isClosed:    false,
		MsgHandler:  msgHandler,
		msgBuffChan: make(chan []byte, 1024),
	}

	return c
}

func (c *Connection) StartWriter() {
	fmt.Println("[Writer Goroutine is running]")
	defer fmt.Println(c.RemoteAddr().String(), "[conn Writer exit!]")

	for {
		select {
		case data, ok := <-c.msgBuffChan:
			if ok {
				if _, err := c.Conn.Write(data); err != nil {
					fmt.Println("Send Buff Data error:, ", err, " Conn Writer exit")
					return
				}
			} else {
				fmt.Println("msgBuffChan is Closed")
				break
			}
		case <-c.ctx.Done():
			return
		}
	}
}

func (c *Connection) StartReader() {
	fmt.Println("[Reader Goroutine is running]")
	defer fmt.Println(c.RemoteAddr().String(), "[conn Reader exit!]")
	defer c.Stop()

	for {
		select {
		case <-c.ctx.Done():
			return
		default:
			headData := make([]byte, c.Server.Packet().GetHeadLen())
			if _, err := io.ReadFull(c.Conn, headData); err != nil {
				fmt.Println("read msg head error ", err)
				return
			}
			msg, err := c.Server.Packet().Unpack(headData)
			if err != nil {
				fmt.Println("unpack error ", err)
				return
			}
			var data []byte
			if msg.GetDataLen() > 0 {
				data = make([]byte, msg.GetDataLen())
				if _, err := io.ReadFull(c.Conn, data); err != nil {
					fmt.Println("read msg data error ", err)
					return
				}
			}
			msg.SetData(data)
			req := Request{
				conn: c,
				msg:  msg,
			}
			c.MsgHandler.SendMsgToTaskQueue(&req)
		}
	}
}

func (c *Connection) Start() {
	c.ctx, c.cancel = context.WithCancel(context.Background())
	go c.StartReader()
	go c.StartWriter()
	select {
	case <-c.ctx.Done():
		c.finalizer()
		return
	}
}

func (c *Connection) Stop() {
	c.cancel()
}

func (c *Connection) GetTCPConnection() *net.TCPConn {
	return c.Conn
}

func (c *Connection) GetConnID() uint32 {
	return c.ConnID
}

func (c *Connection) RemoteAddr() net.Addr {
	return c.Conn.RemoteAddr()
}

func (c *Connection) SendMsg(msgID uint32, data []byte) error {
	c.RLock()
	defer c.RUnlock()
	if c.isClosed == true {
		return errors.New("connection closed when send msg")
	}

	dp := c.Server.Packet()
	msg, err := dp.Pack(NewMessage(msgID, data))
	if err != nil {
		fmt.Println("Pack error msg ID = ", msgID)
		return errors.New("Pack error msg ")
	}
	_, err = c.Conn.Write(msg)
	return err
}

func (c *Connection) SendBuffMsg(msgID uint32, data []byte) error {
	c.RLock()
	defer c.RUnlock()
	idleTimeout := time.NewTimer(5 * time.Millisecond)
	defer idleTimeout.Stop()

	if c.isClosed == true {
		return errors.New("Connection closed when send buff msg")
	}

	dp := c.Server.Packet()
	msg, err := dp.Pack(NewMessage(msgID, data))
	if err != nil {
		fmt.Println("Pack error msg ID = ", msgID)
		return errors.New("Pack error msg ")
	}
	select {
	case <-idleTimeout.C:
		return errors.New("send buff msg timeout")
	case c.msgBuffChan <- msg:
		return nil
	}

	return nil
}

func (c *Connection) Context() context.Context {
	return c.ctx
}

func (c *Connection) finalizer() {

	c.Lock()
	defer c.Unlock()
	if c.isClosed == true {
		return
	}
	fmt.Println("Conn Stop()...ConnID = ", c.ConnID)
	_ = c.Conn.Close()
	c.Server.GetConnMgr().Remove(c)
	close(c.msgBuffChan)
	//设置标志位
	c.isClosed = true
}
