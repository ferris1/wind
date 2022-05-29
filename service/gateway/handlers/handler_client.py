
import logging
from engine.client.ClientMgr import ClientConn
from service.gateway.mgrs.gate_router_mgr import GateRouterMgr
from engine.codec.proto_importer import CreateRoleResponse
import time


# 客户端RPC函数类
class ClientHandlers:
    # 心跳包
    @staticmethod
    async def Handler_HeartbeatRequest(client: ClientConn, request):
        client.last_heartbeat_time = int(time.time())
        logging.info(f"receive client:{client.peer_id} Heartbeat")
    
    # rpc函数以Handler_开头 后面接Protobuf的协议名
    @staticmethod
    async def Handler_PlayerLoginRequest(client: ClientConn, request):
        logging.info(f"player_id:{client}, request:{request} ")
        client.set_player_id(request.player_id)
        GateRouterMgr().on_player_login(request.player_id)
    
    # rpc函数以Handler开头
    @staticmethod
    async def Handler_CreateRoleRequest(client: ClientConn, request):
        logging.info(f"player:{request.player_id} create role:{request.role_id} success")
        res = CreateRoleResponse()
        res.player_id = request.player_id
        res.role_id = request.role_id
        res.result = True
        client.send_packet(res)



