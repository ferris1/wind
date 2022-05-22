
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_name2type = dict()

proto_id2name[6001] = 'S_GameHello'
proto_id2name[6002] = 'S_GameHelloAck'
proto_id2name[6003] = 'S_PlayerRegister'
proto_id2name[6004] = 'S_PlayerRegisterAck'
proto_id2name[6005] = 'S_PlayerUnRegister'
proto_id2name[6006] = 'S_PlayerUnRegisterAck'
proto_name2id['S_GameHello'] = 6001
proto_name2id['S_GameHelloAck'] = 6002
proto_name2id['S_PlayerRegister'] = 6003
proto_name2id['S_PlayerRegisterAck'] = 6004
proto_name2id['S_PlayerUnRegister'] = 6005
proto_name2id['S_PlayerUnRegisterAck'] = 6006
str_S_GameHello = 'S_GameHello'
str_S_GameHelloAck = 'S_GameHelloAck'
str_S_PlayerRegister = 'S_PlayerRegister'
str_S_PlayerRegisterAck = 'S_PlayerRegisterAck'
str_S_PlayerUnRegister = 'S_PlayerUnRegister'
str_S_PlayerUnRegisterAck = 'S_PlayerUnRegisterAck'
proto_name2type['S_GameHello'] = S_GameHello
proto_name2type['S_GameHelloAck'] = S_GameHelloAck
proto_name2type['S_PlayerRegister'] = S_PlayerRegister
proto_name2type['S_PlayerRegisterAck'] = S_PlayerRegisterAck
proto_name2type['S_PlayerUnRegister'] = S_PlayerUnRegister
proto_name2type['S_PlayerUnRegisterAck'] = S_PlayerUnRegisterAck

