from engine.utils.Singleton import Singleton
from engine.utils.Const import SeverType
from engine import SrvEngine
import logging
from engine.codec.proto_importer import S_PlayerRegister,PlayerLoginResponse,S_PlayerUnRegister
from engine.client.ClientMgr import ClientMgr


# 没填的默认路由到game 一般是默认路由到主逻辑服务器
server_router_dict = {
    SeverType.GATEWAY: ["CreateRoleRequest", "HeartbeatRequest", "PlayerLoginRequest"],
    SeverType.GAME: ["SpeakOnWorldRequest"]
}


class GateRouterMgr(Singleton):
    def __init__(self):
        # 协议路由
        self.cmd_router_dict = {}
        # 一般服务器的绑定信息放到redis里  因为每个玩家每类服务器只绑定一个，同时,会有多个服务器访问绑定信息 所以放redis里面
        # 这里为了减少冗余代码，所以每个服有一份绑定信息，如果你要用的话，建议放到redis中
        self.player2server = {}
        self.load_router()

    def on_player_leave(self, player_id):
        logging.info(f"on_player_leave player_id:{player_id}")
        srv_id=  self.get_player_bind_server(player_id)
        if srv_id:
            self.player2server.pop(srv_id,None)
            self.send_unregister_player(player_id, srv_id)

    def send_unregister_player(self, player_id, srv_id):
        sync = S_PlayerUnRegister()
        sync.player_id = player_id
        SrvEngine.srv_inst.send_server_message(SeverType.GAME, srv_id, player_id, sync)

    def load_router(self):
        for typ, lst in server_router_dict.items():
            for proto_name in lst:
                self.cmd_router_dict[proto_name] = typ


    def get_player_bind_server(self, player_id):
        return self.player2server.get(player_id, "*")

    def get_cmd_router_server(self, cmd):
        return self.cmd_router_dict.get(cmd, SeverType.NONE)

    def on_player_login(self, player_id):
        # 先绑定下服务器
        bind_server = self.player2server.get(SeverType.GAME)
        if not bind_server:
            # 由select随机选取一个game服务
            bind_server = SrvEngine.srv_inst.selector.random_choose(SeverType.GAME)
            if not bind_server:
                logging.error("No Game Server to Bind")
                return
            # 绑定Game服务
            self.player2server[player_id] = bind_server
            logging.warning(f"player_id:{player_id} bind game:{bind_server} success ")
        # 发服务器的RPC到Game服务，告诉Game服务有人注册了。
        sync = S_PlayerRegister()
        sync.player_id = player_id
        sync.gate_server_id = SrvEngine.srv_inst.server_id
        SrvEngine.srv_inst.send_server_message(SeverType.GAME, bind_server, player_id, sync)

    def on_register_ack(self, player_id, result):
        if not result:
            return

        res = PlayerLoginResponse()
        res.result = result
        res.player_id = player_id
        client = ClientMgr().get_client_by_player_id(player_id)
        if client:
            logging.info(f"PlayerLoginResponse: {res}")
            client.send_packet(res)
        else:
            logging.error(f"no client of player:{player_id}")





