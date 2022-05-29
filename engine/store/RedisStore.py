
import aioredis

# python的redis客户端使用这个: https://github.com/aio-libs/aioredis-py


class RedisStore:
    def __init__(self):
        self.conn = None
        self.srv_inst = None
        self.pool = None
    
    def init(self, srv_inst):
        self.srv_inst = srv_inst
        self.pool = aioredis.ConnectionPool.from_url(
        "redis://localhost", decode_responses=True)
        self.conn = aioredis.Redis(connection_pool=self.pool)
    
    async def disconnect(self):
        self.pool.disconnect()
