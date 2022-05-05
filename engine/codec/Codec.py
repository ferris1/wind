from engine.utils.Singleton import Singleton
from engine.codec.gen.rpc_client import gen_proto_factory
import logging

class CodecMgr(Singleton):
    def __init__(self):
        pass

    def encode(self, pck):
        data = pck.SerializeToString()
        return data

    def decode(self, proto_name, data):
        typ = self.get_proto_obj(proto_name)
        if typ:
            typ.ParseFromString(data)
        return typ

    def get_proto_name(self, proto_id):
        return gen_proto_factory.proto_id2name.get(proto_id, "")

    def get_proto_id(self, proto_name):
        return gen_proto_factory.proto_name2id.get(proto_name, 0)

    def get_proto_obj(self, proto_name):
        typ = gen_proto_factory.proto_name2type.get(proto_name)
        if typ:
            return typ()
        return None



