import uuid
import asyncio
import logging
from engine.logger.LogModule import init_log
import sys
from engine.utils.Utils import init_asyncio_loop_policy,load_all_handlers
from engine.registry.EtcdRegistry import EtcdRegistry
from engine.broker.NatsBroker import NatsBroker
from engine.broker.BrokerPack import BrokerPack
from engine.utils.Const import SeverType
# python 3.9.12


class Engine:
    def __init__(self, name: str, typ, process_pool: int = None) -> None:
        self.exited = False
        self.server_id: str = uuid.uuid4().hex
        self.sid: bytes = self.server_id.encode()
        self.name: str = name
        self.server_type:int = typ
        self.ip = "127.0.0.1"
        self.port = 0

        self.request_que = asyncio.Queue()
        self.client_cmd_map = {}
        self.server_cmd_map = {}
        init_asyncio_loop_policy()
        self.loop = asyncio.get_event_loop()

        # 以下为各个插件
        init_log(self)
        self.registry = EtcdRegistry()
        self.broker = NatsBroker()

    async def init(self):
        logging.info("SrvEngine Init")
        argv_len = len(sys.argv)
        if argv_len < 2:
            raise ValueError("没有传递可用窗口")
        else:
            self.port = int(sys.argv[1])
        self.registry.init(srv_inst)
        await self.broker.init(srv_inst)

    async def register(self):
        self.register_server_cmd(load_all_handlers('engine.handlers'))
        await self.registry.register(self.server_id, self.server_type)
        await self.broker.subscribe()

    async def start(self):
        await self.registry.watch_servers()

    async def exit(self):
        pass

    async def launch(self):
        # 配置参数
        await self.init()
        # 注册rpc处理函数
        await self.register()
        # 启动前最后做一些逻辑操作等
        await self.start()
        logging.critical(f"################ 服务 {self.name} 启动完毕 ##############")
        logging.info("服务端口号:{}".format(self.port))

    def serve(self):
        logging.getLogger().setLevel(logging.INFO)
        self.loop.run_until_complete(asyncio.ensure_future(self.launch()))
        try:
            self.loop.run_forever()
        except SystemExit:
            logging.info("SYSTEM EXIT 0")
        finally:
            self.loop.close()
            logging.info("loop closed!!")

    def register_client_cmd(self, cmd_dct):
        self.client_cmd_map.update(cmd_dct)

    def register_server_cmd(self, cmd_dct):
        self.server_cmd_map.update(cmd_dct)

    def get_client_cmd(self, name):
        return self.client_cmd_map.get(name)

    def get_server_cmd(self, name):
        return self.server_cmd_map.get(name)

    # 客户端的RPC 处理函数参数默认采用client和request
    async def on_client_request(self, client, cmd, request):
        func = self.get_client_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(client, request)
            else:
                func(client, request)
        else:
            logging.error(f"no rpc func:{cmd}")

    # 服务器的RPC 处理函数参数默认采用pid和pck
    async def on_server_message(self, pid, cmd, pck):
        logging.info(f"on_server_message:pid:{pid}, cmd:{cmd}, pck:{pck}")
        # 优先查看是否是转发过来的客户端包 是的话由客户端来处理
        if self.get_client_cmd(cmd):
            await self.on_client_request(pid, cmd, pck)
            return
        func = self.get_server_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(pid, pck)
            else:
                func(pid, pck)
        else:
            logging.error(f"no rpc func:{cmd}")

    def get_report_info(self):
        info = {
            'ip': self.ip,
            'port': self.port,
        }
        return info

    def on_server_del(self, info):
        logging.error(f"on_server_del.info:{info} ")

    def on_server_add(self, info):
        logging.error(f"on_server_add.info:{info} ")

    # 一般为了节省内部流量 服务器内部消息头不加pid
    async def send_server_message(self, server_type, server_id, pid, pck):
        cmd = pck.DESCRIPTOR.full_name
        data = BrokerPack().pack(pid, cmd, pck)
        if server_id == "*":
            await self.broker.send_to_group_server(server_type, data)
        elif server_id is not None and server_id != "":
            await self.broker.send_to_server(server_id, data)
        else:
            await self.broker.send_to_all_server(data)

    async def send_response_by_gateway(self, pid, pck):
        await self.send_server_message(SeverType.GATEWAY, "*", pid, pck)


# engine 实例
srv_inst: Engine = None
