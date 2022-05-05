
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_id2type = dict()

proto_id2name[1001] = 'PlayerLoginRequest'
proto_id2name[1002] = 'PlayerLoginResponse'
proto_name2id['PlayerLoginRequest'] = 1001
proto_name2id['PlayerLoginResponse'] = 1002
str_PlayerLoginRequest = 'PlayerLoginRequest'
str_PlayerLoginResponse = 'PlayerLoginResponse'
proto_id2type['PlayerLoginRequest'] = PlayerLoginRequest
proto_id2type['PlayerLoginResponse'] = PlayerLoginResponse

