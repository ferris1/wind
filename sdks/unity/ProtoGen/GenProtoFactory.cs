
// do not edit. gen by server codec
using System;
using System.Collections.Generic;
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
					var res1002 = new PlayerLoginResponse();
					return res1002;
				case 1004:
					var res1004 = new CreateRoleResponse();
					return res1004;
				case 1006:
					var res1006 = new SpeakOnWorldResponse();
					return res1006;
				case 1010:
					var res1010 = new PlayerMoveResponse();
					return res1010;
				case 1012:
					var res1012 = new PlayerJoinRoomResponse();
					return res1012;

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

			}
			return 0;
		}	
		public static readonly string HeartbeatRequest_NAME = "HeartbeatRequest";
		public static readonly string PlayerLoginRequest_NAME = "PlayerLoginRequest";
		public static readonly string PlayerLoginResponse_NAME = "PlayerLoginResponse";
		public static readonly string CreateRoleRequest_NAME = "CreateRoleRequest";
		public static readonly string CreateRoleResponse_NAME = "CreateRoleResponse";
		public static readonly string SpeakOnWorldRequest_NAME = "SpeakOnWorldRequest";
		public static readonly string SpeakOnWorldResponse_NAME = "SpeakOnWorldResponse";
		public static readonly string Vector3_NAME = "Vector3";
		public static readonly string Vector2_NAME = "Vector2";
		public static readonly string PlayerMoveRequest_NAME = "PlayerMoveRequest";
		public static readonly string PlayerMoveResponse_NAME = "PlayerMoveResponse";
		public static readonly string PlayerJoinRoomRequest_NAME = "PlayerJoinRoomRequest";
		public static readonly string PlayerJoinRoomResponse_NAME = "PlayerJoinRoomResponse";

	}
}
