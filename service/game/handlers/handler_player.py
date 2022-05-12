
import logging
from service.game.mgrs.game_player_mgr import GamePlayerMgr


# 客户端rpc函数以Handler开头, 服务器
async def Handler_SpeakOnWorldRequest(player_id, request):
    logging.info(f"Handler_SpeakOnWorldRequest:{player_id}, request:{request} ")
    GamePlayerMgr().player_speak_on_world(player_id, request.name, request.content)

