package wnet

import (
	"fmt"
)

type IMsgHandle interface {
	DoMsgHandler(request IRequest)          //马上以非阻塞方式处理消息
	StartWorkerPool()                       //启动worker工作池
	SendMsgToTaskQueue(request IRequest)    //将消息交给TaskQueue,由worker进行处理
}


type MsgHandle struct {
	WorkerPoolSize 		int32                    //业务工作Worker池的数量
	TaskQueue      		[]chan IRequest    //Worker负责取任务的消息队列
}

//NewMsgHandle 创建MsgHandle
func NewMsgHandle() *MsgHandle {
	return &MsgHandle{
		WorkerPoolSize: WorkerPoolSize,
		//一个worker对应一个queue
		TaskQueue: make([]chan IRequest, WorkerPoolSize),
	}
}

//SendMsgToTaskQueue 将消息交给TaskQueue,由worker进行处理
func (mh *MsgHandle) SendMsgToTaskQueue(request IRequest) {
	//根据ConnID来分配当前的连接应该由哪个worker负责处理
	//轮询的平均分配法则

	//得到需要处理此条连接的workerID
	workerID := request.GetConnection().GetConnID() % uint32(mh.WorkerPoolSize)
	//fmt.Println("Add ConnID=", request.GetConnection().GetConnID()," request msgID=", request.GetMsgID(), "to workerID=", workerID)
	//将请求消息发送给任务队列
	mh.TaskQueue[workerID] <- request
}

//DoMsgHandler 马上以非阻塞方式处理消息
func (mh *MsgHandle) DoMsgHandler(request IRequest) {
	//  todo
}


//StartOneWorker 启动一个Worker工作流程
func (mh *MsgHandle) StartOneWorker(workerID int, taskQueue chan IRequest) {
	fmt.Println("Worker ID = ", workerID, " is started.")
	//不断的等待队列中的消息
	for {
		select {
		//有消息则取出队列的Request，并执行绑定的业务方法
		case request := <-taskQueue:
			mh.DoMsgHandler(request)
		}
	}
}

//StartWorkerPool 启动worker工作池
func (mh *MsgHandle) StartWorkerPool() {
	//遍历需要启动worker的数量，依此启动
	for i := 0; i < int(mh.WorkerPoolSize); i++ {
		//一个worker被启动
		//给当前worker对应的任务队列开辟空间
		mh.TaskQueue[i] = make(chan IRequest, MaxWorkerTaskLen)
		//启动当前Worker，阻塞的等待对应的任务队列是否有消息传递进来
		go mh.StartOneWorker(i, mh.TaskQueue[i])
	}
}
