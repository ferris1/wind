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
        // 客户端请求队列
        private ConcurrentQueue<ClientRequest> RequestQue;
        // 服务器消息队列
        private ConcurrentQueue<ServerMessage> MessageQue;

        // 心跳
        private float lastHeatbeatTime = 0;
        
        private HeartbeatRequest heatbeat = new HeartbeatRequest();

        // 连接
        private float connectTime = 0;
     

        // 客户端请求
        public delegate bool RequestFunc(object o);
        private sealed class ClientRequest
        {
            public RequestFunc RequestFunc = null;
            public object Data;
        }
        // 服务器处理函数
        public delegate void HandlerFunc(object o);
        class ServerMessage
        {
            public HandlerFunc Handler = null;
            public object Data;
        }

        private Agent()
        {
            RequestQue = new ConcurrentQueue<ClientRequest>();
            MessageQue = new ConcurrentQueue<ServerMessage>();
            thread = new Thread(RequestThread);
            thread.Start();
            tcp = new TCPConn(this);
            ResetConn();
        }

        public static Agent GetInstance()
        {

            if (_instance == null)
            {
                _instance = new Agent();
            }
            return _instance;
        }

        #region Connect
        private static readonly RequestFunc ConnectFunc = (o) =>
        {
            GetInstance().tcp.Connect(GetInstance().ip, GetInstance().port);

            return true;
        };
        public void ConnectToServer(string _ip, int _port)
        {
            ip = _ip;
            port = _port;
            connectTime = Time.realtimeSinceStartup;
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
        
        private void CheckSendHeatbeat()
        {
            var now = Time.realtimeSinceStartup;
            if ( now - lastHeatbeatTime > Const.HeatBeatTime && isConnected)
            {
                Debug.Log("send heatbeat");
                SendRequest(heatbeat);
                lastHeatbeatTime = now;
            }
        }

        // 网络线程  处理发送数据与接受数据
        private void RequestThread()
        {
            Thread.CurrentThread.Name = "WindNetwork";
            while (!stopped)
            {
                try
                {
                    
                    // 处理发送的数据
                    ClientRequest request;
                    while (RequestQue.TryDequeue(out request))
                    {
                        lock (connectionLock)
                        {
                            var data = request.RequestFunc(request.Data);
                        }
                    }
                    // 处理接受数据
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

        public void CheckConnectTimeOut()
        {
            if(!isConnected && connectTime!=0 && Time.realtimeSinceStartup - connectTime > Const.ConnectTimeOut)
            {
                OnConnectTimeOut();
            }
        }

        // 主线程调用，网络线程的包会回调到主线线程
        public void NetUpdate()
        {
            CheckConnectTimeOut();
            ServerMessage msg;
            while (MessageQue.TryDequeue(out msg))
            {
                msg.Handler(msg.Data);
            }
            // 发送心跳
            CheckSendHeatbeat();
        }

        public void Disconnect()
        {
            if (isConnected)
            {
                ResetConn();
                tcp.socket.Close();
            }
        }

        public void OnConnectCallback(bool succ)
        {
            Debug.Log($"OnConnectCallback succ: {succ}");
            if (succ)
            {
                isConnected = true;
                connectTime = 0;
                GameMgr.inst.OnNetConnect(succ);
            }
        }

        public void OnDisconnectCallback()
        {

        }

        public void OnConnectTimeOut()
        {
            Debug.LogError("Connect Timeout");
            ResetConn();
            tcp.socket.Close();
        }

        public void ResetConn()
        {
            isConnected = false;
            connectTime = 0;
        }
    }
}