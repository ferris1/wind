
import logging
from engine.codec.proto_importer import PlayerLoginResponse
from engine.client.ClientMgr import ClientConn


# 客户端rpc函数以Handler开头
async def Handler_PlayerLoginRequest(client: ClientConn, request):
    logging.info(f"player_id:{client}, request:{request} ")
    client.set_player_id(request.player_id)
    pck = PlayerLoginResponse()
    pck.player_id = request.player_id
    pck.result = True
    client.send_packet(pck)

