from engine.utils.Singleton import Singleton
from engine.codec.proto_importer import S_PlayerRegisterAck, S_PlayerUnRegisterAck, SpeakOnWorldResponse,\
    PlayerMoveResponse,PlayerJoinRoomResponse,PlayerUpdateTransformResponse
from engine import SrvEngine
from engine.utils.Const import SeverType
import logging

class GamePlayerMgr(Singleton):
    def __init__(self):
        self.player2server = {}

    def get_player_bind_server(self, player_id):
        return self.player2server.get(player_id, "*")

    def on_player_register(self, player_id, gate_server_id):
        if player_id in self.player2server:
            logging.error(f"player:{player_id} always bind server:{self.player2server[player_id]}")
            result = False
        else:
            self.player2server[player_id] = gate_server_id
            result = True
        sync = S_PlayerRegisterAck()
        sync.result = result
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

    def player_move(self, player_id, request):
        for other_id, svr in self.player2server.items():
            res = PlayerMoveResponse()
            res.player_id = player_id
            res.move.CopyFrom(request.move)
            res.look.CopyFrom(request.look)
            SrvEngine.srv_inst.send_response_by_gateway(other_id, res, sid=svr)

    def player_join_room(self, player_id):
        for other_id, svr in self.player2server.items():
            res = PlayerJoinRoomResponse()
            res.player_id = player_id
            res.result = True
            SrvEngine.srv_inst.send_response_by_gateway(other_id, res, sid=svr)

    def player_update_transform(self, player_id, request):
        for other_id, svr in self.player2server.items():
            res = PlayerUpdateTransformResponse()
            res.player_id = player_id
            res.position.CopyFrom(request.position)
            res.rotation.CopyFrom(request.rotation)
            SrvEngine.srv_inst.send_response_by_gateway(other_id, res, sid=svr)