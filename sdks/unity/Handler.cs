using System;
using UnityEngine;
using System.Collections.Generic;


public static partial class WindHandler
{
    public static void On_PlayerLoginResponse(PlayerLoginResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
    }
    public static void On_CreateRoleResponse(CreateRoleResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
    }
    public static void On_SpeakOnWorldResponse(SpeakOnWorldResponse pck)
    {
        Debug.Log($"recv packet:{pck}");
    }

}

