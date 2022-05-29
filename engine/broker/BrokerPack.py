from engine.utils.Singleton import Singleton
from engine.codec.gen.proto_client import factory_client
from engine.codec.gen.proto_server import factory_server
from engine.utils.Utils import uint32_to_bytes,uint_from_bytes


class BrokerPack(Singleton):
    def __init__(self):
        pass

    def pack(self, pid, cmd, pck):
        if pid is None:
            pid = ""
        data = bytearray()
        msg_id = self.get_proto_id(cmd)
        data += uint32_to_bytes(msg_id)
        data += uint32_to_bytes(len(pid))
        if len(pid) > 0:
            data += pid.encode()
        data += pck.SerializeToString()
        return data

    def unpack(self, data):
        msg_id = uint_from_bytes(data[0:4])
        cmd = self.get_proto_name(msg_id)
        p_len = uint_from_bytes(data[4:8])
        if p_len > 0:
            pid = data[8:8+p_len].decode()
        else:
            pid = ""
        obj_data = data[8+p_len:]
        pck = self.get_proto_obj(cmd)
        if pck:
            pck.ParseFromString(obj_data)
        return pid, cmd, pck

    def get_proto_name(self, proto_id):
        name = factory_client.proto_id2name.get(proto_id, "")
        if name:
            return name
        return factory_server.proto_id2name.get(proto_id, "")

    def get_proto_id(self, proto_name):
        _id = factory_client.proto_name2id.get(proto_name, 0)
        if _id:
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


