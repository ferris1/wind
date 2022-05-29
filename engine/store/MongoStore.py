
# 异步的Mongo客户端使用这个: hhttps://github.com/mongodb/motor
import motor


class MongoStore:
    def __init__(self):
        self.conn = None
        self.srv_inst = None
        
    def init(self, srv_inst):
        self.srv_inst = srv_inst
        self.conn = motor.MotorClient("localhost", 27017)

