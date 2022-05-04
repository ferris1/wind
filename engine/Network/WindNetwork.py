
import asyncio
from engine import SrvEngine
import ctypes
import logging
from engine.network.NetMessage import MsgPack,Message
from engine.utils.Const import ServerCmdEnum
from engine.utils.Utils import check_async_cb


class WindNetwork:

    __slots__ = ["net_srv", "net_proto", "network_dll", "on_connect_callback", "on_disconnect_callback",
                 "on_packet_callback", "net_status", "net_transport"]

    def __init__(self):
        self.net_srv = None
        self.net_proto = None
        self.network_dll = None
        self.on_connect_callback = None
        self.on_disconnect_callback = None
        self.on_packet_callback = None
        self.net_status = False
        self.net_transport = None

    async def start_net_thread(self, ip, port, net_connect_callback, net_disconnect_callback, net_packet_callback):
        self.on_connect_callback = check_async_cb(net_connect_callback)
        self.on_disconnect_callback = check_async_cb(net_disconnect_callback)
        self.on_packet_callback = check_async_cb(net_packet_callback)
        self.net_status = False
        self.net_srv = await SrvEngine.srv_inst.loop.create_server(lambda: NetProtocol(self), "127.0.0.1", port+10)
        net_thread_address = f'{ip}:{port+10}'
        dll_file = r'../builds/wnet.dll'

        self.network_dll = ctypes.WinDLL(dll_file)
        self.network_dll.StartNetThread.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.network_dll.StartNetThread.restype = ctypes.c_void_p

        self.network_dll.StartNetThread(net_thread_address.encode(), ip.encode(), SrvEngine.srv_inst.name.encode(), port)

    def net_send_data(self, peer_id, data):
        if not self.net_transport:
            logging.error(" no net transport")
            return
        mess = Message()
        mess.cmd_id = ServerCmdEnum.CmdSend.value
        mess.data = data
        mess.peer_id = peer_id
        mess.msg_id = 0
        raw_data = MsgPack().pack(mess)
        logging.info(f"net_send_data.peer_id:{peer_id}, data:{data}")
        self.net_transport.write(raw_data)


class NetProtocol(asyncio.Protocol):

    def __init__(self, net):
        super().__init__()
        self.transport = None
        self.net = net

    def connection_lost(self, exc):
        pass

    def connection_made(self, transport):
        self.transport = transport
        self.net.net_transport = transport
        logging.info(f"connection_made.transport:{self.transport} ")

    def data_received(self, data):
        mess = MsgPack().unpack(data)
        if mess.cmd_id == ServerCmdEnum.CmdInit.value:
            self.net.net_status = True
            new = Message()
            new.cmd_id = ServerCmdEnum.CmdInit.value
            data = MsgPack().pack(new)
            self.transport.write(data)
        elif mess.cmd_id == ServerCmdEnum.CmdConnect.value:
            # 端口用msg_id替代   ip跟在data里
            ip = str(mess.data)
            self.net.on_connect_callback(mess.peer_id, ip, mess.msg_id)
        elif mess.cmd_id == ServerCmdEnum.CmdDisconnect.value:
            self.net.on_disconnect_callback(mess.peer_id)
        elif mess.cmd_id == ServerCmdEnum.CmdPacket.value:
            self.net.on_packet_callback(mess.peer_id, mess.msg_id, mess.data_len, mess.data)

    def eof_received(self):
        pass

    def exit(self):
        self.transport.close()

