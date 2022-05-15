
import logging
from engine.client.ClientMgr import ClientConn
from service.gateway.mgrs.gate_router_mgr import GateRouterMgr
from engine.codec.proto_importer import CreateRoleResponse

# 客户端rpc函数以Handler开头  如果是直连客户端的服务器 第一个参数是client否者是player_id
async def Handler_HeartbeatRequest(client: ClientConn, request):
    logging.info(f"receive client:{client.peer_id} Heartbeat")


# 客户端rpc函数以Handler_开头 后面接Protobuf的协议名
async def Handler_PlayerLoginRequest(client: ClientConn, request):
    logging.info(f"player_id:{client}, request:{request} ")
    client.set_player_id(request.player_id)
    GateRouterMgr().on_player_login(request.player_id)


# 客户端rpc函数以Handler开头
async def Handler_CreateRoleRequest(client: ClientConn, request):
    logging.info(f"player:{request.player_id} create role:{request.role_id} success")
    res = CreateRoleResponse()
    res.player_id = request.player_id
    res.role_id = request.role_id
    res.result = True
    client.send_packet(res)



