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
from engine.utils import Const
import time

class ClientStatus(IntEnum):
    NONE = 0
    CONNECTED = 1
    DISCONNECTED = 2


class ClientConn:
    __slots__ = ['address', 'port', 'peer_id', 'player_id', 'session_key', 'timestamp', 'status',
                 'session_key', 'srv', 'last_heartbeat_time']

    def __init__(self):
        self.address = None
        self.port = None
        self.peer_id = None
        self.player_id = ""
        self.session_key = None
        self.timestamp = None
        self.status = ClientStatus.NONE
        self.srv = None
        self.last_heartbeat_time = 0

    def send_packet(self, pck):
        mess = Message()
        mess.cmd_id = ServerCmdEnum.CmdSend.value
        mess.data = CodecMgr().encode(pck)
        mess.peer_id = self.peer_id
        mess.msg_id = CodecMgr().get_proto_id(pck.DESCRIPTOR.name)
        raw_data = MsgPack().pack(mess)
        # logging.info(f" send_packet:{mess}")
        ClientMgr().wind_net.net_send_data(raw_data)

    def disconnect(self):
        self.status = ClientStatus.DISCONNECTED

    def set_player_id(self, player_id):
        self.player_id = player_id
        ClientMgr().set_player_id(player_id, self)


class ClientMgr(Singleton):
    def __init__(self):
        self.peer_to_client = {}
        self.player_id_to_client = {}
        self.connect_count = 0
        self.wind_net: WindNetwork = None

    async def init(self, ip, port):
        logging.info("ClientMgr init ")
        self.wind_net = WindNetwork()
        await self.wind_net.start_net_worker(ip, port, self.on_net_connect, self.on_net_disconnect, self.on_net_data)

    def update(self):
        peer_lst = list(self.peer_to_client.keys())
        now = int(time.time())
        
        for peer_id in peer_lst:
            conn = self.get_client_conn_by_peer(peer_id)
            if now - conn.last_heartbeat_time > Const.GatewayHeartTimeOut:
                self.on_peer_heartbeat_time_out(peer_id)

    def on_peer_heartbeat_time_out(self, peer_id):
        logging.warning(f"on_peer_heartbeat_time_out.peer_id:{peer_id}")
        client = self.get_client_conn_by_peer(peer_id)
        SrvEngine.srv_inst.on_client_disconect(client.player_id)
        self.peer_to_client.pop(peer_id, None)
        self.connect_count -= 1

    # ??????????????????????????? ??????callback?????????
    def on_net_connect(self, peer_id, address, port):
        logging.info(f"on_net_connect.peer_id:{peer_id},address:{address}, port:{port}")
        client = self.create_conn(peer_id, address, port)
        client.status = ClientStatus.CONNECTED
        client.last_heartbeat_time = time.time()
        self.peer_to_client[peer_id] = client
        self.connect_count += 1

    def on_net_disconnect(self, peer_id):
        logging.info(f"on_net_disconnect.peer_id:{peer_id}")
        client = self.get_client_conn_by_peer(peer_id)
        SrvEngine.srv_inst.on_client_disconect(client.player_id)
        self.peer_to_client.pop(peer_id, None)
        self.connect_count -= 1

    def on_net_data(self, peer_id, proto_id, proto_data_len, proto_data):
        # logging.info(f"on_net_data.peer_id:{peer_id},proto_id:{proto_id}, proto_data_len:{proto_data_len}")
        client = self.get_client_conn_by_peer(peer_id)
        if client:
            client.last_heartbeat_time = time.time()
            cmd = CodecMgr().get_proto_name(proto_id)
            request = CodecMgr().decode(cmd, proto_data)
            asyncio.ensure_future(SrvEngine.srv_inst.on_client_request(client, cmd, request))

    def create_conn(self, peer_id, address, port):
        conn = ClientConn()
        conn.address = address
        conn.peer_id = peer_id
        conn.port = port
        return conn

    def get_client_conn_by_peer(self, peer_id) -> ClientConn:
        return self.peer_to_client.get(peer_id)

    def get_client_by_player_id(self, player_id) -> ClientConn:
        return self.player_id_to_client.get(player_id)

    def deal_command(self):
        pass

    def disconnect_client(self, conn):
        pass

    def set_player_id(self, player_id, client):
        self.player_id_to_client[player_id] = client


