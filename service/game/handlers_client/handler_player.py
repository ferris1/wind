
import logging
from engine.codec.proto_importer import CreateRoleResponse
from engine import SrvEngine

# 客户端rpc函数以Handler开头, 服务器
async def Handler_CreateRoleRequest(player_id, request):
    logging.info(f"player_id:{player_id}, request:{request} ")
    pck = CreateRoleResponse()
    pck.player_id = request.player_id
    pck.result = True
    await SrvEngine.srv_inst.send_response_by_gateway(player_id, pck)
