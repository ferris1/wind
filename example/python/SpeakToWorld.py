import asyncio
from engine.codec.proto_importer import PlayerLoginRequest,CreateRoleRequest, SpeakOnWorldRequest
from engine.codec.Codec import CodecMgr
from engine.utils.Utils import uint_from_bytes, uint32_to_bytes
from engine.utils.Singleton import Singleton
import uuid

class ClientMessage:
    __slots__ = ["msg_id", "data_len", "data"]

    def __init__(self):
        self.msg_id = 0
        self.data_len = 0
        self.data = bytearray()

    def __str__(self):
        return f"msg_id:{self.msg_id}, self.data_len:{self.data_len}, data:{self.data}"


class ClientMsgPack(Singleton):
    def __init__(self):
        pass

    def pack(self, mess:ClientMessage):
        data = bytearray()
        data += uint32_to_bytes(mess.msg_id)
        data += uint32_to_bytes(len(mess.data))
        data += mess.data
        return data

    def unpack(self, data, index):
        mess = ClientMessage()
        mess.msg_id = uint_from_bytes(data[index:index+4])
        mess.data_len = uint_from_bytes(data[index+4:index+8])
        mess.data = data[index+8:index+8+mess.data_len]
        index+8+mess.data_len
        return mess, index


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        print(f'connection_made: {transport}')

    def data_received(self, data):
        mess, index = ClientMsgPack().unpack(data, 0)
        cmd = CodecMgr().get_proto_name(mess.msg_id)
        obj = CodecMgr().decode(cmd, mess.data)
        print(f"receive:{cmd}, data:{obj}")

    def connection_lost(self, exc):
        print('The server closed the connection')


def send_pack(transport, pck):
    msg_id = CodecMgr().get_proto_id(pck.DESCRIPTOR.name)
    mess = ClientMessage()
    mess.msg_id = msg_id
    mess.data = CodecMgr().encode(pck)
    data = ClientMsgPack().pack(mess)
    transport.write(data)


def send_player_login(player_id, transport):
    req = PlayerLoginRequest()
    req.player_id = player_id
    send_pack(transport, req)
    print(f"player:{player_id} send login")


def send_create_role(player_id, transport):
    req = CreateRoleRequest()
    req.player_id = player_id
    req.role_id = 1010
    send_pack(transport, req)
    print(f"player:{player_id} send create role:{req.role_id}")


def send_speak_world(player_id, name, transport):
    req = SpeakOnWorldRequest()
    req.player_id = player_id
    req.name = name
    req.content = "hello, i'm wind!"
    send_pack(transport, req)
    print(f"player:{player_id} speak world:{req.content}")


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(),
        '127.0.0.1', 50100)

    await asyncio.sleep(3)
    player_id = uuid.uuid4().hex
    name = "name_"+player_id[-4:]
    send_player_login(player_id, transport)
    await asyncio.sleep(1)

    send_create_role(player_id, transport)
    await asyncio.sleep(1)

    while True:
        send_speak_world(player_id, name, transport)
        await asyncio.sleep(2)


asyncio.run(main())