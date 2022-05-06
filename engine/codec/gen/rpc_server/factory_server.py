
from engine.codec.proto_importer import *

proto_id2name = dict()
proto_name2id = dict()
proto_name2type = dict()

proto_id2name[6001] = 'S_GameHello'
proto_id2name[6002] = 'S_GameHelloAck'
proto_name2id['S_GameHello'] = 6001
proto_name2id['S_GameHelloAck'] = 6002
str_S_GameHello = 'S_GameHello'
str_S_GameHelloAck = 'S_GameHelloAck'
proto_name2type['S_GameHello'] = S_GameHello
proto_name2type['S_GameHelloAck'] = S_GameHelloAck

