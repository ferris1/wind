from engine.utils.Singleton import Singleton
from engine.codec.gen.proto_client import factory_client
from engine.codec.gen.proto_server import factory_server


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
        name = factory_client.proto_id2name.get(proto_id, "")
        if name:
            return name
        return factory_server.proto_id2name.get(proto_id, "")

    def get_proto_id(self, proto_name):

        _id = factory_client.proto_name2id.get(proto_name, 0)
        import logging

        if _id != 0:
            return _id
        return factory_server.proto_name2id.get(proto_name, 0)

    def get_proto_obj(self, proto_name):
        typ = factory_client.proto_name2type.get(proto_name, None)
        if typ:
            return typ()
        typ = factory_server.proto_name2type.get(proto_name)
        if typ:
            return typ()
        return None



