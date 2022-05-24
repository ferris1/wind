
import logging
from service.game.mgrs.game_player_mgr import GamePlayerMgr


# 客户端rpc函数以Handler开头, 服务器
async def Handler_SpeakOnWorldRequest(player_id, request):
    logging.info(f"Handler_SpeakOnWorldRequest:{player_id}, request:{request} ")
    GamePlayerMgr().player_speak_on_world(player_id, request.name, request.content)


# 客户端rpc函数以Handler开头, 服务器
async def Handler_PlayerMoveRequest(player_id, request):
    # logging.info(f"Handler_PlayerMoveRequest:{player_id}, request:{request} ")
    GamePlayerMgr().player_move(player_id, request)


# 客户端rpc函数以Handler开头, 服务器
async def Handler_PlayerJoinRoomRequest(player_id, request):
    logging.info(f"Handler_PlayerJoinRoomRequest:{player_id}, request:{request} ")
    GamePlayerMgr().player_join_room(player_id)

# 客户端rpc函数以Handler开头, 服务器
async def Handler_PlayerUpdateTransformRequest(player_id, request):
    # logging.info(f"Handler_PlayerUpdateTransformRequest:{player_id}, request:{request} ")
    GamePlayerMgr().player_update_transform(player_id, request)