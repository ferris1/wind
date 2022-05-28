
using System;
using System.Collections.Generic;
using UnityEngine;

namespace WindNetwork
{
    class MsgPack
    {
       
        public static MsgPack inst = null;
        private readonly int HeadLen = 8;

        public static MsgPack GetInstance
        {
            get
            {
                if (inst == null)
                    inst = new MsgPack();
                return inst;
            }
        }


        public int GetHeadLen()
        {
            return HeadLen;
        }

        public int UnpackLen(byte[] data, int readPos)
        {
            var msgId = BitConverter.ToInt32(data, readPos);
            readPos += 4;
            var len = BitConverter.ToInt32(data, readPos);
            return len;
        }

        public Message Unpack(byte[] data, int readPos)
        {
            var mess = new Message();
            mess.SetMsgId(BitConverter.ToInt32(data, readPos));
            mess.SetDataLen(BitConverter.ToInt32(data, readPos + 4));
            return mess;
        }

        public byte[] Pack(Message mess)
        {
            var buffer = new List<byte>();
            buffer.AddRange(BitConverter.GetBytes(mess.GetMsgId()));
            buffer.AddRange(BitConverter.GetBytes(mess.GetDataLen()));
            buffer.AddRange(mess.GetData());
            return buffer.ToArray();
        }
    }
}
