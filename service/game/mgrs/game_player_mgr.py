from engine.utils.Singleton import Singleton
from engine.codec.proto_importer import S_PlayerRegisterAck, S_PlayerUnRegisterAck, SpeakOnWorldResponse
from engine import SrvEngine
from engine.utils.Const import SeverType


class GamePlayerMgr(Singleton):
    def __init__(self):
        # 绑定Gate服
        # 一般服务器的绑定信息放到redis里  因为每个玩家每类服务器只绑定一个，同时会有多个服务器访问绑定信息 所以放redis里面比较合理
        # 这里为了减少冗余代码，所以每个服有一份绑定信息，如果你要用的话，建议放到redis中
        self.player2server = {}

    def get_player_bind_server(self, player_id):
        return self.player2server.get(player_id, "*")

    def on_player_register(self, player_id, gate_server_id):
        self.player2server[player_id] = gate_server_id
        sync = S_PlayerRegisterAck()
        sync.result = True
        SrvEngine.srv_inst.send_server_message(SeverType.GATEWAY, gate_server_id, player_id, sync)

    def on_player_unregister(self, player_id):
        gate_server_id = self.player2server.pop(player_id, None)
        if gate_server_id:
            sync = S_PlayerUnRegisterAck()
            sync.result = True
            SrvEngine.srv_inst.send_server_message(SeverType.GATEWAY, gate_server_id, player_id, sync)

    def player_speak_on_world(self, player_id, name, content):
        for other_id, svr in self.player2server.items():
            res = SpeakOnWorldResponse()
            res.speak_id = player_id
            res.name = name
            res.content = content
            SrvEngine.srv_inst.send_response_by_gateway(other_id, res, sid=svr)


