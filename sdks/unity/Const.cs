using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WindNetwork
{
    class Const
    {
        public const float HeatBeatTime = 3; // 每三秒一次心跳
        public const float ConnectTimeOut = 3; // 连接超时时间
        public const int TcpMaxBufferSize = 1024 * 1024;
    }
}
