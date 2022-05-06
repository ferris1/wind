from enum import IntEnum
from engine.utils.Singleton import Singleton
import logging
from engine.network.WindNetwork import WindNetwork
from engine import SrvEngine
import asyncio
from engine.codec.Codec import CodecMgr
from engine.network.NetMessage import Message
from engine.utils.Const import ServerCmdEnum
from engine.network.NetMessage import MsgPack

class ClientStatus(IntEnum):
    NONE = 0
    CONNECTED = 1
    DISCONNECTED = 2


class ClientMgr(Singleton):
    def __init__(self):
        self.peer_to_client = {}
        self.player_id_to_client = {}
        self.connect_count = 0
        self.wind_net: WindNetwork = None

    async def init(self, ip, port):
        logging.info("ClientMgr init ")
        self.wind_net = WindNetwork()
        await self.wind_net.start_net_thread(ip, port, self.on_net_connect, self.on_net_disconnect, self.on_net_data)

    def on_net_connect(self, peer_id, address, port):
        logging.info(f"on_net_connect.peer_id:{peer_id},address:{address}, port:{port}")
        conn = self.create_conn(peer_id, address, port)
        conn.status = ClientStatus.CONNECTED
        self.peer_to_client[peer_id] = conn
        self.connect_count += 1

    def on_net_disconnect(self, peer_id):
        logging.info(f"on_net_disconnect.peer_id:{peer_id}")
        self.peer_to_client.pop(peer_id, None)
        self.connect_count -= 1

    def on_net_data(self, peer_id, proto_id, proto_data_len, proto_data):
        logging.info(f"on_net_data.peer_id:{peer_id},proto_id:{proto_id}, proto_data_len:{proto_data_len}")
        client = self.get_client_conn_by_peer(peer_id)
        if client:
            cmd = CodecMgr().get_proto_name(proto_id)
            request = CodecMgr().decode(cmd, proto_data)
            asyncio.ensure_future(SrvEngine.srv_inst.on_client_request(client, cmd, request))

    def create_conn(self, peer_id, address, port):
        conn = ClientConn()
        conn.address = address
        conn.peer_id = peer_id
        conn.port = port
        return conn

    def get_client_conn_by_peer(self, peer_id):
        return self.peer_to_client.get(peer_id)

    def get_client_by_player_id(self, player_id):
        return self.player_id_to_client.get(player_id)

    def deal_command(self):
        pass

    def disconnect_client(self, conn):
        pass

    def set_player_id(self, player_id, client):
        self.player_id_to_client[player_id] = client


class ClientConn:
    __slots__ = ['address', 'port', 'peer_id', 'player_id', 'session_key', 'timestamp', 'status',
                 'session_key', 'srv']

    def __init__(self):
        self.address = None
        self.port = None
        self.peer_id = None
        self.player_id = ""
        self.session_key = None
        self.timestamp = None
        self.status = ClientStatus.NONE
        self.srv = None

    def send_packet(self, pck):
        mess = Message()
        mess.cmd_id = ServerCmdEnum.CmdSend.value
        mess.data = CodecMgr().encode(pck)
        mess.peer_id = self.peer_id
        mess.msg_id = CodecMgr().get_proto_id(pck.DESCRIPTOR.full_name)
        raw_data = MsgPack().pack(mess)
        logging.info(f" send_packet:{mess}")
        ClientMgr().wind_net.net_send_data(raw_data)

    def disconnect(self):
        self.status = ClientStatus.DISCONNECTED

    def set_player_id(self, player_id):
        self.player_id = player_id
        ClientMgr().set_player_id(player_id,self)
