
using UnityEngine;


public static partial class WindHandler
{
    public static void On_PlayerLoginResponse(WindNetwork.PlayerLoginResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
        // 服务器回包后，客户端逻辑可以在这里加 比如，登录成功后 开始游戏
        GameMgr.inst.OnStartGame();
    }
    public static void On_CreateRoleResponse(WindNetwork.CreateRoleResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
    }
    public static void On_SpeakOnWorldResponse(WindNetwork.SpeakOnWorldResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
        GameMgr.inst.OnPlayerSpeak(pck);
        
    }
    public static void On_PlayerMoveResponse(WindNetwork.PlayerMoveResponse pck)
    {
        //Debug.Log($"recv packet:{pck}");
        GameMgr.inst.OnPlayerMove(pck);
    }
    public static void On_PlayerJoinRoomResponse(WindNetwork.PlayerJoinRoomResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
        GameMgr.inst.OnPlayerJoinRoom(pck);
    }
    public static void On_PlayerUpdateTransformResponse(WindNetwork.PlayerUpdateTransformResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
        GameMgr.inst.OnPlayerUpdateTransform(pck);
    }

}

