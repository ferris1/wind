import asyncio
import logging, struct
import random
import time

import aiozmq, zmq
from engine import SrvEngine
import ctypes
from engine.utils.utils import check_async_cb, uint_from_bytes, int_from_bytes


class ZmqNetwork:
    __slots__ = [
        'enet_connect_callback', 'enet_disconnect_callback', 'enet_packet_callback',
        'zmq_to_netthread_transport', 'zmq_from_netthread_transport', 'netthread_status',
        'network_dll', 'ping_interval', 'enet_heartbeat_timeout_callback'
    ]

    def __init__(self):
        # enet事件
        self.enet_connect_callback = None
        self.enet_disconnect_callback = None
        self.enet_packet_callback = None
        self.enet_heartbeat_timeout_callback = lambda peer_id, b_timeout: None

        # asyncio zmq connection to net thread
        self.zmq_to_netthread_transport = None
        self.zmq_from_netthread_transport = None
        self.netthread_status: bool = False

        self.ping_interval = 30  # 控制客户端Ping的频率

        # dll
        self.network_dll = None

    async def start_net_thread(self, ip:str, port, enet_connect_callback, enet_disconnect_callback, enet_packet_callback):
        # 等网络线程返回INIT消息后才会设置为True
        self.netthread_status = False
        srv = SrvEngine.srv_inst
        dll_file = r'../builds/wnet.dll'
        self.network_dll = ctypes.WinDLL(dll_file)
        self.network_dll.StartNetThread.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.network_dll.StartNetThread.restype = ctypes.c_void_p
        zmq_to_net_thread_address = 'tcp://127.0.0.1:60000'
        zmq_from_net_thread_address = 'tcp://127.0.0.1:60010'
        ip = ip.encode()

        self.enet_connect_callback = check_async_cb(enet_connect_callback)
        self.enet_disconnect_callback = check_async_cb(enet_disconnect_callback)
        self.enet_packet_callback = check_async_cb(enet_packet_callback)

        logging.info("connect to net thread")
        sock_to = zmq.Context.instance().socket(zmq.PUSH)
        sock_to.setsockopt(zmq.SNDHWM, 0)
        sock_to.setsockopt(zmq.SNDBUF, 10*1024*1024)
        sock_to.setsockopt(zmq.LINGER, 3000)
        self.zmq_to_netthread_transport, _ = await aiozmq.create_zmq_connection(
            aiozmq.ZmqProtocol, zmq.PUSH,
            bind=zmq_to_net_thread_address, zmq_sock=sock_to, loop=srv.loop)

        sock_from = zmq.Context.instance().socket(zmq.PULL)
        sock_from.setsockopt(zmq.RCVHWM, 0)
        sock_from.setsockopt(zmq.RCVBUF, 10*1024*1024)
        sock_from.setsockopt(zmq.LINGER, 3000)
        self.zmq_from_netthread_transport, _ = await aiozmq.create_zmq_connection(
            lambda: ZmqFromNetThreadProtocol(self), zmq.PULL,
            bind=zmq_from_net_thread_address, zmq_sock=sock_from, loop=srv.loop)

        logging.info("StartNetThread")
        self.network_dll.StartNetThread(zmq_to_net_thread_address.encode(), zmq_from_net_thread_address.encode(), ip, port)
        return True


class ZmqFromNetThreadProtocol(aiozmq.ZmqProtocol):
    __slots__ = ['transport', 'net']

    def __init__(self, server_net):
        self.transport = None
        self.net = server_net

    def connection_made(self, transport):
        self.transport = transport

    def msg_received(self, data):
        try:
            command = data[0]
            if command == b'PAKT':
                cid = uint_from_bytes(data[1])
                proto_id = int_from_bytes(data[2])
                proto_data_len = int_from_bytes(data[3])
                self.net.enet_packet_callback(cid, proto_id, proto_data_len, data[4])
            elif command == b'CONN':
                cid = uint_from_bytes(data[1])
                port = int_from_bytes(data[3])
                self.net.enet_connect_callback(cid, data[2], port)
            elif command == b'DISC':
                cid = uint_from_bytes(data[1])
                self.net.enet_disconnect_callback(cid)
            elif command == b'INIT':
                if self.net.netthread_status is False:
                    self.net.netthread_status = True
                    self.net.zmq_to_netthread_transport.write([b'INIT'])
            elif command == b'HBTO':  # heartbeat timeout
                cid = uint_from_bytes(data[1])
                b_time_out = bool.from_bytes(data[2], byteorder="little")
                self.net.enet_heartbeat_timeout_callback(cid, b_time_out)
            else:
                # TODO: unknown command
                pass
        except Exception as e:
            pass

    # print('from net thread data: ' + str(data))

    def connection_lost(self, exc):
        logging.info('inbound connection lost from net thread' + str(exc))
