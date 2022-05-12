
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_name2type = dict()

proto_id2name[101] = 'HeartbeatRequest'
proto_id2name[1001] = 'PlayerLoginRequest'
proto_id2name[1002] = 'PlayerLoginResponse'
proto_id2name[1003] = 'CreateRoleRequest'
proto_id2name[1004] = 'CreateRoleResponse'
proto_id2name[1005] = 'SpeakOnWorldRequest'
proto_id2name[1006] = 'SpeakOnWorldResponse'
proto_name2id['HeartbeatRequest'] = 101
proto_name2id['PlayerLoginRequest'] = 1001
proto_name2id['PlayerLoginResponse'] = 1002
proto_name2id['CreateRoleRequest'] = 1003
proto_name2id['CreateRoleResponse'] = 1004
proto_name2id['SpeakOnWorldRequest'] = 1005
proto_name2id['SpeakOnWorldResponse'] = 1006
str_HeartbeatRequest = 'HeartbeatRequest'
str_PlayerLoginRequest = 'PlayerLoginRequest'
str_PlayerLoginResponse = 'PlayerLoginResponse'
str_CreateRoleRequest = 'CreateRoleRequest'
str_CreateRoleResponse = 'CreateRoleResponse'
str_SpeakOnWorldRequest = 'SpeakOnWorldRequest'
str_SpeakOnWorldResponse = 'SpeakOnWorldResponse'
proto_name2type['HeartbeatRequest'] = HeartbeatRequest
proto_name2type['PlayerLoginRequest'] = PlayerLoginRequest
proto_name2type['PlayerLoginResponse'] = PlayerLoginResponse
proto_name2type['CreateRoleRequest'] = CreateRoleRequest
proto_name2type['CreateRoleResponse'] = CreateRoleResponse
proto_name2type['SpeakOnWorldRequest'] = SpeakOnWorldRequest
proto_name2type['SpeakOnWorldResponse'] = SpeakOnWorldResponse

