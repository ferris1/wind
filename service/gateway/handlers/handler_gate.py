from engine.codec.proto_importer import S_PlayerRegisterAck
import logging
from service.gateway.mgrs.gate_router_mgr import GateRouterMgr


# 服务器RPC函数类
class ServerHandlers:
    # rpc函数以Handler开头, 服务器的中间有个S
    @staticmethod
    async def Handler_S_PlayerRegisterAck(player_id, request:S_PlayerRegisterAck):
        logging.info(f"S_PlayerRegisterAc player_id:{player_id}, request:{request} ")
        GateRouterMgr().on_register_ack(player_id, request.result)
