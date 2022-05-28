
// do not edit. gen by server codec
using Google.Protobuf;

namespace WindNetwork
{
	public partial class ProtoFactoryPb
	{
		public static IMessage GetProtoObj(int protoId)
		{
			switch (protoId)
			{
				case 1002:
					var proto1002 = new PlayerLoginResponse();
					return proto1002;
				case 1004:
					var proto1004 = new CreateRoleResponse();
					return proto1004;
				case 1006:
					var proto1006 = new SpeakOnWorldResponse();
					return proto1006;
				case 1010:
					var proto1010 = new PlayerMoveResponse();
					return proto1010;
				case 1012:
					var proto1012 = new PlayerJoinRoomResponse();
					return proto1012;
				case 1014:
					var proto1014 = new PlayerUpdateTransformResponse();
					return proto1014;

			}
			return null;
		}

		public static IMessage DecodeProtoData(byte[] dataBytes, int protoId)
		{
			IMessage ret;
			switch (protoId)
			{
				case 1002:
					ret = PlayerLoginResponse.Parser.ParseFrom(dataBytes);
					return ret;
				case 1004:
					ret = CreateRoleResponse.Parser.ParseFrom(dataBytes);
					return ret;
				case 1006:
					ret = SpeakOnWorldResponse.Parser.ParseFrom(dataBytes);
					return ret;
				case 1010:
					ret = PlayerMoveResponse.Parser.ParseFrom(dataBytes);
					return ret;
				case 1012:
					ret = PlayerJoinRoomResponse.Parser.ParseFrom(dataBytes);
					return ret;
				case 1014:
					ret = PlayerUpdateTransformResponse.Parser.ParseFrom(dataBytes);
					return ret;

			}
			return null;
		}

		public static void Call(int protoId, IMessage m)
		{
			switch (protoId)
			{
				case 1002:
					WindHandler.On_PlayerLoginResponse((PlayerLoginResponse)m);
				break;
				case 1004:
					WindHandler.On_CreateRoleResponse((CreateRoleResponse)m);
				break;
				case 1006:
					WindHandler.On_SpeakOnWorldResponse((SpeakOnWorldResponse)m);
				break;
				case 1010:
					WindHandler.On_PlayerMoveResponse((PlayerMoveResponse)m);
				break;
				case 1012:
					WindHandler.On_PlayerJoinRoomResponse((PlayerJoinRoomResponse)m);
				break;
				case 1014:
					WindHandler.On_PlayerUpdateTransformResponse((PlayerUpdateTransformResponse)m);
				break;

			}
		}	

		public static int GetProtoId(string name)
		{
			switch (name)
			{
				case "HeartbeatRequest":
					return 101;
				case "PlayerLoginRequest":
					return 1001;
				case "PlayerLoginResponse":
					return 1002;
				case "CreateRoleRequest":
					return 1003;
				case "CreateRoleResponse":
					return 1004;
				case "SpeakOnWorldRequest":
					return 1005;
				case "SpeakOnWorldResponse":
					return 1006;
				case "Vector3":
					return 1007;
				case "Vector2":
					return 1008;
				case "PlayerMoveRequest":
					return 1009;
				case "PlayerMoveResponse":
					return 1010;
				case "PlayerJoinRoomRequest":
					return 1011;
				case "PlayerJoinRoomResponse":
					return 1012;
				case "PlayerUpdateTransformRequest":
					return 1013;
				case "PlayerUpdateTransformResponse":
					return 1014;

			}
			return 0;
		}
	}
}
