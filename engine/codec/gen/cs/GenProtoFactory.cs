
using System;
using System.Collections.Generic;
using Google.Protobuf;

namespace NetworkCodec
{
	public partial class ProtoFactoryPb
	{
		public static IMessage GetProtoObj(int proto_id)
		{
			switch (proto_id)
			{
				case 1002:
					var res1002 = new PlayerLoginResponse();
					return res1002;

			}
			return null;
		}

		public static IMessage GetProtoObj(byte[] _buf, ref int idx, out int proto_id)
		{
			proto_id = Misc.short_from_bytes_le(_buf, ref idx);
			int data_size = Misc.int_from_bytes_le(_buf, ref idx);
			var data_sequence = new byte[data_size];
			Array.Copy(_buf, idx, data_sequence, 0, data_sequence.Length);
			idx += data_size;
			IMessage ret;
			switch (proto_id)
			{
				case 1002:
					ret = PlayerLoginResponse.Parser.ParseFrom(data_sequence);
					return ret;

			}
			return null;
		}

		public static void Call(int protoId, IMessage m)
		{
			switch (protoId)
			{
				case 1002:
					ServerRpcImplement.On_PlayerLoginResponse((PlayerLoginResponse)m);
				break;

			}
		}	

		public static int GetProtoId(string name)
		{
			switch (name)
			{
				case "PlayerLoginRequest":
					return 1001;
				case "PlayerLoginResponse":
					return 1002;

			}
			return 0;
		}	
		public static readonly string PlayerLoginRequest_NAME = "PlayerLoginRequest";
		public static readonly string PlayerLoginResponse_NAME = "PlayerLoginResponse";

	}
}
