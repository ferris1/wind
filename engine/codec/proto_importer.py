
# 因为各个协议的protobuf文件是分离的,写代码时不好处理,所以这里手动统一import以下,方便写逻辑。
from engine.codec.gen.proto_client.Player_pb2 import *
from engine.codec.gen.proto_server.Game_pb2 import *
from engine.codec.gen.proto_client.Engine_pb2 import *
from engine.codec.gen.proto_client.Room_pb2 import *
