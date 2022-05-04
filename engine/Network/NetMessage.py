
from engine.utils.Singleton import Singleton
from engine.utils.Const import ServerCmdEnum
from engine.utils.Utils import uint_from_bytes,uint32_to_bytes
import logging

class Message:
    __slots__ = ["msg_id", "cmd_id", "data_len", "data"]

    def __init__(self):
        self.msg_id = 0
        self.cmd_id = ServerCmdEnum.CmdNone
        self.data_len = 0
        self.data = bytearray()

    def __str__(self):
        return f"msg_id:{self.msg_id}, cmd_id:{self.cmd_id}, self.data_len:{self.data_len}, data:{self.data}"


class MsgPack(Singleton):
    def __init__(self):
        pass

    def pack(self, mess:Message):
        data = bytearray()
        data += uint32_to_bytes(mess.cmd_id)
        data += uint32_to_bytes(mess.msg_id)
        data += uint32_to_bytes(len(mess.data))
        data += mess.data
        return data

    def unpack(self, data):
        mess = Message()
        mess.cmd_id = uint_from_bytes(data[0:4])
        mess.msg_id = uint_from_bytes(data[4:8])
        mess.data_len = uint_from_bytes(data[8:12])
        mess.data = data[12:]
        return mess


