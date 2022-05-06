
from engine.utils.Singleton import Singleton
from engine.utils.Const import ServerCmdEnum
from engine.utils.Utils import uint_from_bytes, uint32_to_bytes


class Message:
    __slots__ = ["msg_id", "cmd_id", "data_len", "data", "peer_id"]

    def __init__(self):
        self.msg_id = 0
        self.cmd_id = ServerCmdEnum.CmdNone
        self.data_len = 0
        self.peer_id = 0
        self.data = bytearray()

    def __str__(self):
        return f"msg_id:{self.msg_id}, cmd_id:{self.cmd_id}, self.data_len:{self.data_len}, data:{self.data}"


class MsgPack(Singleton):
    def __init__(self):
        pass

    def pack(self, mess:Message):
        data = bytearray()
        data += uint32_to_bytes(mess.cmd_id)
        data += uint32_to_bytes(mess.peer_id)
        data += uint32_to_bytes(mess.msg_id)
        data += uint32_to_bytes(len(mess.data))
        data += mess.data
        return data

    def unpack(self, data, index):
        mess = Message()
        mess.cmd_id = uint_from_bytes(data[index:index+4])
        mess.peer_id = uint_from_bytes(data[index+4:index+8])
        mess.msg_id = uint_from_bytes(data[index+8:index+12])
        mess.data_len = uint_from_bytes(data[index+12:index+16])
        mess.data = data[index+16:index+16+mess.data_len]
        index = index+16+mess.data_len
        return mess, index


