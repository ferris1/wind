
from enum import IntEnum


class ServerCmdEnum(IntEnum):
    CmdNone = 0
    CmdInit = 1
    CmdConnect = 2
    CmdDisconnect = 3
    CmdPacket = 4

    CmdSend = 100
    CmdExit = 101


class SeverType:
    NONE = 0
    GAME = 1
    GATEWAY = 2

    ALLSERVER = 100


class MessageType:
    ServerMessage = 1
    PlayerRequest = 2
    PlayerResponse = 3
    UnknownMessage = 100

# 限制包体类型 因为转发包给客户端时 是通过这个设置的

def GET_MESSAGE_TYPE(command):
    if command[0:2] == 'S_':
        return MessageType.ServerMessage
    elif command[-7:] == 'Request':
        return MessageType.PlayerRequest
    elif command[-8:] == 'Response':
        return MessageType.PlayerResponse
    else:
        return MessageType.UnknownMessage

