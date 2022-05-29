
import logging
from service.game.mgrs.game_player_mgr import GamePlayerMgr
from engine.codec.proto_importer import S_PlayerRegister, S_PlayerUnRegister


# 服务器RPC函数类
class ServerHandlers:
    # rpc函数以Handler开头, 服务器的中间有个S
    @staticmethod
    async def Handler_S_PlayerRegister(player_id, request:S_PlayerRegister):
        logging.info(f"Handler_S_PlayerRegister player_id:{player_id}, request:{request} ")
        GamePlayerMgr().on_player_register(player_id, request.gate_server_id)
    
    # rpc函数以Handler开头, 服务器的中间有个S
    @staticmethod
    async def Handler_S_PlayerUnRegister(player_id, request:S_PlayerUnRegister):
        logging.info(f"Handler_S_PlayerUnRegister player_id:{player_id}, request:{request} ")
        GamePlayerMgr().on_player_unregister(player_id)


