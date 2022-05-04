
import asyncio
from engine import SrvEngine
import ctypes
import logging
from engine.network.NetMessage import MsgPack,Message
from engine.utils.Const import ServerCmdEnum

class WindNetwork:

    __slots__ = ["net_srv", "net_proto", "network_dll"]

    def __init__(self):
        self.net_srv = None
        self.net_proto = None
        self.network_dll = None

    async def start_net_thread(self, ip, port, net_connect_callback, net_disconnect_callback, net_packet_callback):
        to_net_thread_address = 'tcp://127.0.0.1:60000'
        from_net_thread_address = 'tcp://127.0.0.1:60010'
        self.net_srv = await SrvEngine.srv_inst.loop.create_server(lambda: NetProtocol(self), "127.0.0.1", 60010)

        dll_file = r'../builds/wnet.dll'
        self.network_dll = ctypes.WinDLL(dll_file)
        self.network_dll.StartNetThread.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.network_dll.StartNetThread.restype = ctypes.c_void_p

        ip = ip.encode()

        self.network_dll.StartNetThread(to_net_thread_address.encode(), from_net_thread_address.encode(), ip,
                                        port)


class NetProtocol(asyncio.Protocol):

    def __init__(self, net):
        super().__init__()
        self.transport = None
        self.net = net

    def connection_lost(self, exc):
        pass

    def connection_made(self, transport):
        self.transport = transport
        logging.info(f"connection_made.transport:{self.transport} ")

    def data_received(self, data):
        mess = MsgPack().unpack(data)
        if mess.cmd_id == ServerCmdEnum.CmdInit.value:
            new = Message()
            new.cmd_id = ServerCmdEnum.CmdInit.value
            data = MsgPack().pack(new)
            self.transport.write(data)

    def eof_received(self):
        pass

    def exit(self):
        self.transport.close()

