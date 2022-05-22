using System;

using Google.Protobuf;

namespace WindNetwork
{
    class Message
    {
        private int msgId;
        private int dataLen;
        private byte[] byteData;
        public IMessage pbObj;

        public int GetMsgId()
        {
            return msgId;
        }
        public int GetDataLen()
        {
            return dataLen;
        }
        public byte[] GetData()
        {
            return byteData;
        }

        public void SetMsgId(int Id)
        {
            msgId = Id;
        }
        public void SetDataLen(int len)
        {
            dataLen = len;
        }
        public void SetData(byte[] data,int startIndex,int len)
        {
            byteData = new byte[len];
            Buffer.BlockCopy(data, startIndex, byteData, 0, len);
        }
    }
}
