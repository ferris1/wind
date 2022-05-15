
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

			}
			return null;
		}

		public static void Call(int protoId, IMessage m)
		{
			switch (protoId)
			{

			}
		}	

		public static int GetProtoId(string name)
		{
			switch (name)
			{
				case "S_GameHello":
					return 6001;
				case "S_GameHelloAck":
					return 6002;
				case "S_PlayerRegister":
					return 6003;
				case "S_PlayerRegisterAck":
					return 6004;
				case "S_PlayerUnRegister":
					return 6005;
				case "S_PlayerUnRegisterAck":
					return 6006;

			}
			return 0;
		}	
		public static readonly string S_GameHello_NAME = "S_GameHello";
		public static readonly string S_GameHelloAck_NAME = "S_GameHelloAck";
		public static readonly string S_PlayerRegister_NAME = "S_PlayerRegister";
		public static readonly string S_PlayerRegisterAck_NAME = "S_PlayerRegisterAck";
		public static readonly string S_PlayerUnRegister_NAME = "S_PlayerUnRegister";
		public static readonly string S_PlayerUnRegisterAck_NAME = "S_PlayerUnRegisterAck";

	}
}
