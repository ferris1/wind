
import logging
from engine.client.ClientMgr import ClientConn


# rpc 函数以Handler开头
def Handler_PlayerLoginRequest(client:ClientConn, request):
    logging.info(f"request:{request} ")
    data = request.encode()
    client.send_packet(data)
