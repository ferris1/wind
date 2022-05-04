package wnet

import (
	"errors"
	"fmt"
	"sync"
)

type IConnManager interface {
	Add(conn IConnection)
	Remove(conn IConnection)
	Get(connID uint32) (IConnection, error)
	Len() int32
	ClearConn()
}

type ConnManager struct {
	connections map[uint32]IConnection
	connLock    sync.RWMutex
}

func NewConnManager() IConnManager {
	return &ConnManager{
		connections: make(map[uint32]IConnection),
	}
}

func (connMgr *ConnManager) Add(conn IConnection) {
	connMgr.connLock.Lock()
	connMgr.connections[conn.GetPeerID()] = conn
	connMgr.connLock.Unlock()

	fmt.Println("connection add to ConnManager successfully: conn num = ", connMgr.Len())
}

func (connMgr *ConnManager) Remove(conn IConnection) {

	connMgr.connLock.Lock()
	delete(connMgr.connections, conn.GetPeerID())
	connMgr.connLock.Unlock()
	fmt.Println("connection Remove PeerID=", conn.GetPeerID(), " successfully: conn num = ", connMgr.Len())
}

func (connMgr *ConnManager) Get(connID uint32) (IConnection, error) {
	connMgr.connLock.RLock()
	defer connMgr.connLock.RUnlock()

	if conn, ok := connMgr.connections[connID]; ok {
		return conn, nil
	}

	return nil, errors.New("connection not found")

}

func (connMgr *ConnManager) Len() int32 {
	connMgr.connLock.RLock()
	length := len(connMgr.connections)
	connMgr.connLock.RUnlock()
	return int32(length)
}

func (connMgr *ConnManager) ClearConn() {
	connMgr.connLock.Lock()

	for connID, conn := range connMgr.connections {
		conn.Stop()
		delete(connMgr.connections, connID)
	}
	connMgr.connLock.Unlock()
	fmt.Println("Clear All Connections successfully: conn num = ", connMgr.Len())
}

func (connMgr *ConnManager) ClearOneConn(connID uint32) {
	connMgr.connLock.Lock()
	defer connMgr.connLock.Unlock()

	connections := connMgr.connections
	if conn, ok := connections[connID]; ok {
		conn.Stop()
		delete(connections, connID)
		fmt.Println("Clear Connections MsgID:  ", connID, "succeed")
		return
	}

	fmt.Println("Clear Connections MsgID:  ", connID, "err")
	return
}

