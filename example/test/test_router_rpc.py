import asyncio
from engine.codec.proto_importer import PlayerLoginRequest,CreateRoleRequest
from engine.codec.Codec import CodecMgr
from engine.utils.Utils import uint_from_bytes, uint32_to_bytes
from engine.utils.Singleton import Singleton


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
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost
        self.transport = None

    def connection_made(self, transport):
        print('connection_made: {!r}'.format(self.message))

    def data_received(self, data):
        mess, index = ClientMsgPack().unpack(data, 0)
        cmd = CodecMgr().get_proto_name(mess.msg_id)
        obj = CodecMgr().decode(cmd, mess.data)
        print(f"mess:{mess}, obj:{obj}")

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)



async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    on_con_lost = loop.create_future()
    message = 'Hello World!'

    transport, protocol = await loop.create_connection(
        lambda: EchoClientProtocol(message, on_con_lost),
        '127.0.0.1', 50100)
    req = PlayerLoginRequest()
    req.player_id = "ferris1/wind"
    msg_id = CodecMgr().get_proto_id(req.DESCRIPTOR.name)
    mess = ClientMessage()
    mess.msg_id = msg_id
    mess.data = CodecMgr().encode(req)
    print(f"send mess:{mess}")
    data = ClientMsgPack().pack(mess)
    transport.write(data)

    await asyncio.sleep(3)

    req = CreateRoleRequest()
    req.player_id = "ferris1/wind"
    msg_id = CodecMgr().get_proto_id(req.DESCRIPTOR.name)
    mess = ClientMessage()
    mess.msg_id = msg_id
    mess.data = CodecMgr().encode(req)
    print(f"send mess:{mess}")
    data = ClientMsgPack().pack(mess)
    transport.write(data)
    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


asyncio.run(main())