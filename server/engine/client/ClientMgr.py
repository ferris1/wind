from enum import IntEnum
from engine.utils.Singleton import Singleton
import logging


class ClientMgr(Singleton):

    def __init__(self):
        self.peer_to_client = {}
        self.connect_count = 0
        self.connect_cb = None
        self.disconnet_cb = None
        self.data_cb = None

    def init(self, connect_cb, disconnet_cb, data_cb):
        logging.info("ClientMgr init ")

    def on_net_connect(self, peer_id, address, port):
        conn = self.create_conn(peer_id,address,port)
        self.peer_to_client[peer_id] = conn
        self.connect_count += 1
        if self.connect_cb:
            self.connect_cb(peer_id)

    def on_net_disconnect(self, peer_id):
        self.peer_to_client.pop(peer_id,None)
        self.connect_count -= 1
        if self.disconnet_cb:
            self.disconnet_cb(peer_id)

    def on_net_data(self, peer_id, proto_id, proto_data_len, proto_data):
        pass

    def create_conn(self, peer_id, address, port):
        conn = ClientConn()
        conn.address = address
        conn.peer_id = peer_id
        conn.port = port
        return conn

    def get_client_conn_by_peer(self, peer_id):
        return self.peer_to_client.get(peer_id)

    def deal_command(self):
        pass

    # 主动断开
    def disconnect_client(self, conn):
        pass

class ClientStatus(IntEnum):
    CONNECTED = 0
    DISCONNECTED = 1


class ClientConn:
    __slots__ = ['address', 'port', 'peer_id', 'player_id', 'session_key', 'timestamp', 'status',
                 'session_key', 'srv']

    def __init__(self):
        self.address = None
        self.port = None
        self.peer_id = None
        self.player_id = None
        self.session_key = None
        self.timestamp = None
        self.status = ClientStatus.CONNECTED
        self.client_mgr = None
        self.srv = None

    def send_packet(self, pck):
        pass

    def disconnect(self):
        self.status = ClientStatus.DISCONNECTED

