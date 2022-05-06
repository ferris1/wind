
import logging
from engine.client.ClientMgr import ClientConn
from engine.codec.proto_importer import PlayerLoginResponse


# rpc 函数以Handler开头
def Handler_PlayerLoginRequest(client:ClientConn, request):
    logging.info(f"request:{request} ")
    pck = PlayerLoginResponse()
    pck.player_id = request.player_id
    pck.result = True
    client.send_packet(pck)
