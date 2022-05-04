
from enum import IntEnum


class ServerCmdEnum(IntEnum):
    CmdNone = 0
    CmdInit = 1
    CmdConnect = 2
    CmdDisconnect = 3
    CmdPacket = 4

    CmdSend = 100
    CmdExit = 101
