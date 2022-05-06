
# 使用这个 https://github.com/nats-io/nats.py
from engine.config.IpConfig import NATS_ADDR
import nats
from nats.errors import Error, TimeoutError, NoServersError
import logging
from engine.utils.Const import SeverType
from functools import partial


class NatsBroker:
    def __init__(self):
        self.nats_c:nats.NATS = None
        self.connect_status = False
        self.srv_inst = None

    async def init(self, srv_inst):
        self.srv_inst = srv_inst
        try:
            self.nats_c = await nats.connect(NATS_ADDR, allow_reconnect=False, max_reconnect_attempts=1)
        except NoServersError as e:
            logging.error("no nats server. please launch nats server first. see "
                          "https://docs.nats.io/running-a-nats-service/introduction/installation")
        except (OSError, Error, TimeoutError) as e:
            logging.error("no nats server. please launch nats server first. see "
                          "https://docs.nats.io/running-a-nats-service/introduction/installation")
        else:
            self.connect_status = True
            logging.info(f"connect NATS_ADDR:{NATS_ADDR} success")

    async def subscribe(self):
        if not self.connect_status or not self.nats_c:
            return
        # 监听种类服务消息
        sub = await self.nats_c.subscribe(str(self.srv_inst.server_type), cb=partial(self.on_nats_message, self))
        # 监听所有服务消息
        sub = await self.nats_c.subscribe(str(SeverType.ALLSERVER), cb=partial(self.on_nats_message, self))
        # 监听指定给自己
        sub = await self.nats_c.subscribe(self.srv_inst.server_id, cb=partial(self.on_nats_message, self))

    async def on_nats_message(self, msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data
        await self.srv_inst.on_server_message(msg.data)
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    async def send_to_server(self, server_id, data):
        await self.nats_c.publish(server_id, data)

    async def send_to_group_server(self, server_type, data):
        await self.nats_c.publish(str(server_type), data)

    async def send_to_all_server(self, data):
        await self.nats_c.publish(str(SeverType.ALLSERVER), data)




