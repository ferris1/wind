using System;
using System.Net;
using System.Net.Sockets;
using UnityEngine;
using Google.Protobuf;

namespace WindNetwork
{
    public class TCPConn
    {
        public TcpClient socket;
        bool isConnected = false;
        private Agent agent;
        private NetworkStream stream;
        private byte[] receiveBuffer;
        public static int dataBufferSize = 1024 * 1024;  // 1M的缓存
        private int dataIndex = 0, dataOffset = 0;
        
        public TCPConn(Agent data)
        {
            agent = data;
        }

        public void Connect(string ip, int port)
        {
            socket = new TcpClient
            {
                ReceiveBufferSize = dataBufferSize,
                SendBufferSize = dataBufferSize
            };

            receiveBuffer = new byte[dataBufferSize];
            socket.BeginConnect(ip, port, ConnectCallback, socket);
        }

        private void ConnectCallback(IAsyncResult _result)
        {
            socket.EndConnect(_result);

            if (!socket.Connected)
            {
                return;
            }
            
            // 回调到主线程的Callback
            agent.CallOnMainThread(OnConnectCallBackFunc, new ConnectCallbackArgs
            {
                succ = true,
            });
            isConnected = true;
            stream = socket.GetStream();
        }
        class ConnectCallbackArgs
        {
            public bool succ;
        }
        private static readonly Agent.HandlerFunc OnConnectCallBackFunc = o =>
        {
            var data = o as ConnectCallbackArgs;
            Agent.GetInstance().OnConnectCallback(data.succ);
        };

        public bool SendData(IMessage msg)
        {
            try
            {
                if (socket != null && stream != null)
                {
                    
                    var mess = new Message();
                    var protoData = msg.ToByteArray();
                    mess.SetData(protoData, 0, protoData.Length);
                    mess.SetMsgId(ProtoFactoryPb.GetProtoId(msg.Descriptor.Name));
                    mess.SetDataLen(protoData.Length);
                    var byteData = MsgPack.GetInstance.Pack(mess);
                    stream.Write(byteData, 0, byteData.Length); 
                }
            }
            catch (Exception _ex)
            {
                Debug.Log($"Error sending data to server via TCP: {_ex}");
                return false;
            }
            return true;
        }

        public void NetUpdate()
        {
            if (socket != null && stream != null && stream.CanRead)
            {
                bool needReset = false;
                while (stream.DataAvailable)
                {
                    if (dataOffset + 1024 > Const.TcpMaxBufferSize)
                    {
                        needReset = true;
                        break;
                    }
                    int readLen = stream.Read(receiveBuffer, dataOffset, 1024);
                    dataOffset += readLen;
                }
                while (dataOffset - dataIndex > MsgPack.GetInstance.GetHeadLen())
                {
                    
                    var len = MsgPack.GetInstance.UnpackLen(receiveBuffer, dataIndex);
                    if (len > Const.TcpMaxBufferSize)
                    {
                        Debug.LogError($"receive message data over:{Const.TcpMaxBufferSize}. ");
                        return;
                    }
                    if (dataOffset - dataIndex >= len + MsgPack.GetInstance.GetHeadLen())         
                    {
                        var mess = MsgPack.GetInstance.Unpack(receiveBuffer, dataIndex);
                        Debug.Log($"NetUpdate recv mess:{mess.GetMsgId()}");
                        dataIndex += MsgPack.GetInstance.GetHeadLen();
                        mess.SetData(receiveBuffer, dataIndex, mess.GetDataLen());
                        dataIndex += mess.GetDataLen();
                        OnDealMessage(mess);
                    }
                    else
                    {
                        break;
                    }
                }
                if (dataOffset == dataIndex)  
                {
                    dataOffset = 0;
                    dataIndex = 0;
                }
                else if (needReset) 
                {
                    Buffer.BlockCopy(receiveBuffer, dataIndex, receiveBuffer, 0, dataOffset - dataIndex);
                    dataIndex = 0;
                    dataOffset = dataOffset - dataIndex;
                }
            }
        }

        private void OnDealMessage(Message mess)
        {
            agent.CallOnMainThread(ServerMessageFunc, mess);
        }

        private static readonly Agent.HandlerFunc ServerMessageFunc = o =>
        {
            try
            {
                var packData = o as Message;
                // 这个序列化 其实可以放在网络线程处理
                var obj = ProtoFactoryPb.DecodeProtoData(packData.GetData(), packData.GetMsgId());
                ProtoFactoryPb.Call(packData.GetMsgId(), obj);
            }
            catch (Exception e)
            {
                Debug.LogError("call server handler error");
            }
        };

        private void Disconnect()
        {
            Agent.GetInstance().Disconnect();
            stream = null;
            receiveBuffer = null;
            socket = null;
        }
    }
}
