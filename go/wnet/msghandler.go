package wnet

import (
	"fmt"
)

type IMsgHandle interface {
	DoMsgHandler(request IRequest)
	StartWorkerPool()
	SendMsgToTaskQueue(request IRequest)
}


type MsgHandle struct {
	WorkerPoolSize 		int32
	TaskQueue      		[]chan IRequest
}

func NewMsgHandle() *MsgHandle {
	return &MsgHandle{
		WorkerPoolSize: WorkerPoolSize,
		TaskQueue: make([]chan IRequest, WorkerPoolSize),
	}
}

func (mh *MsgHandle) SendMsgToTaskQueue(request IRequest) {

	workerID := request.GetConnection().GetConnID() % uint32(mh.WorkerPoolSize)
	mh.TaskQueue[workerID] <- request
}


func (mh *MsgHandle) DoMsgHandler(request IRequest) {
	fmt.Println("request.id: ",request.GetMsgID(), "data: ", string(request.GetData()))
}


func (mh *MsgHandle) StartOneWorker(workerID int, taskQueue chan IRequest) {
	fmt.Println("Worker ID = ", workerID, " is started.")
	for {
		select {
		case request := <-taskQueue:
			mh.DoMsgHandler(request)
		}
	}
}

func (mh *MsgHandle) StartWorkerPool() {
	for i := 0; i < int(mh.WorkerPoolSize); i++ {
		mh.TaskQueue[i] = make(chan IRequest, MaxWorkerTaskLen)
		go mh.StartOneWorker(i, mh.TaskQueue[i])
	}
}
