using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Threading.Tasks;
using System.Threading;
using System;
using System.Collections.Concurrent;
using Google.Protobuf;

namespace WindNetwork
{
    public  class Agent
    {
        private static Agent _instance;
        public string ip = "127.0.0.1";
        public int port = 50100;
        public int myId = 0;
        
        private bool stopped = false;
        private bool isConnected = false;

        private readonly object connectionLock = new object();
        public TCPConn tcp;

        private readonly Thread thread;

        // �ͻ����������
        private ConcurrentQueue<ClientRequest> RequestQue;
        // ��������Ϣ����
        private ConcurrentQueue<ServerMessage> MessageQue;

        // �ͻ�������
        public delegate bool RequestFunc(object o);
        private sealed class ClientRequest
        {
            public RequestFunc RequestFunc = null;
            public object Data;
        }
        // ������������
        public delegate void HandlerFunc(object o);
        class ServerMessage
        {
            public HandlerFunc Handler = null;
            public object Data;
        }

        private Agent()
        {
            MsgPack.GenInstance();
            RequestQue = new ConcurrentQueue<ClientRequest>();
            MessageQue = new ConcurrentQueue<ServerMessage>();
            thread = new Thread(RequestThread);
            thread.Start();
            tcp = new TCPConn(this);
            isConnected = false;
        }

        public static Agent GetInstance()
        {

            if (_instance == null)
            {
                Debug.LogError($"instance is:{_instance}");
            }
            return _instance;
        }

        public static void GenInstance()
        {

            if (_instance != null)
            {
                Debug.Log("re Gen Agent instance");
                return;
            }
            _instance = new Agent();
        }

        #region Connect
        private static readonly RequestFunc ConnectFunc = (o) =>
        {
            GetInstance().tcp.Connect(GetInstance().ip, GetInstance().port);
            GetInstance().isConnected = true;
            return true;
        };
        public void ConnectToServer()
        {
            AddNetworkThreadTask(ConnectFunc);
        }
        #endregion

        #region Send
        private sealed class SendData
        {
            public IMessage ProtoData;
        }

        private static readonly RequestFunc SendRequestFunc = (o) =>
        {
            var data = o as SendData;
            return GetInstance().tcp.SendData(data.ProtoData);
        };

        public bool SendRequest(IMessage protoObj)
        {
            AddNetworkThreadTask(SendRequestFunc, new SendData
            {
                ProtoData = protoObj,
            });
            return true;
        }
        #endregion

        private void AddNetworkThreadTask(RequestFunc func, object o = null)
        {
            var req = new ClientRequest();
            req.Data = o;
            req.RequestFunc = func;
            RequestQue.Enqueue(req);
        }
        
        // �����߳�  �������������������
        private void RequestThread()
        {
            Thread.CurrentThread.Name = "Network";
            while (!stopped)
            {
                try
                {
                    // �����͵�����
                    ClientRequest request;
                    while (RequestQue.TryDequeue(out request))
                    {
                        lock (connectionLock)
                        {
                            var data = request.RequestFunc(request.Data);
                        }

                    }
                    // �����������
                    if (tcp != null)
                    {
                        lock (connectionLock)
                        {
                            tcp.NetUpdate();
                        }
                    }
                }
                catch (Exception e)
                {
                    Debug.LogError("Network Thread Exception: " + e.ToString());
                    throw;
                }
            }
        }

        public void CallOnMainThread(HandlerFunc f, object o = null)
        {
            var msg = new ServerMessage();
            msg.Handler = f;
            msg.Data = o;
            MessageQue.Enqueue(msg);
        }

        // ���̵߳��ã������̵߳İ���ص��������߳�
        public void NetUpdate()
        {
            ServerMessage msg;
            while (MessageQue.TryDequeue(out msg))
            {
                msg.Handler(msg.Data);
            }
           
        }
       
        public void Disconnect()
        {
            if (isConnected)
            {
                isConnected = false;
                tcp.socket.Close();
                Debug.Log("Disconnected from server.");
            }
        }

      
        public void OnConnectCallback(bool succ)
        {
            Debug.Log($"OnConnectCallback succ: {succ}");
            if(succ)
                GameMgr.inst.OnNetConnect(succ);
        }

        public void OnDisconnectCallback()
        {

        }
    }
}