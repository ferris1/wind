import uuid
import asyncio
import logging
from functools import wraps

from engine.logger.LogModule import init_log
import sys
from engine.utils.Utils import init_asyncio_loop_policy,load_all_handlers
from engine.registry.EtcdRegistry import EtcdRegistry
from engine.broker.NatsBroker import NatsBroker
from engine.broker.BrokerPack import BrokerPack
from engine.utils.Const import SeverType
from engine.selector.Selector import Selector
import asyncio
from engine.config import Config
# python 3.9.12


# Wind的核心类,engine目录下所有的组件都是附加到Engine类的
class Engine:
    def __init__(self, name: str, typ, process_pool: int = None) -> None:
        self.exited = False
        self.server_id: str = uuid.uuid4().hex
        self.sid: bytes = self.server_id.encode()
        self.name: str = name
        self.server_type:int = typ
        self.ip = "127.0.0.1"
        self.port = 0
        self.is_external = False    # 标识是否是对外服务器  如果是的话会有ClientMgr组件,也就是直接与客户端连接的服务器
        self.request_que = asyncio.Queue()
        self.client_cmd_map = {}
        self.server_cmd_map = {}
        init_asyncio_loop_policy()
        self.loop = asyncio.get_event_loop()

        # 以下为各个插件

        self.registry = EtcdRegistry()
        self.broker = NatsBroker()
        self.selector = Selector()

    async def init(self):
        init_log(self)
        logging.info("SrvEngine Init")
        argv_len = len(sys.argv)
        if argv_len < 3:
            raise ValueError("not valid argv: port IsSingle ")
        else:
            self.port = int(sys.argv[1])
        # 是否是单机版本 nats 连接出错的时候 还不能try except
        if sys.argv[2] == "True":
            Config.LaunchSingle(True)
        if Config.USE_ETCD:
            await self.registry.init(srv_inst)
        if Config.USE_NATS:
            await self.broker.init(srv_inst)
        self.selector.init(self.registry)

    async def register(self):
        client_cmd, server_cmd = load_all_handlers('engine.handlers')
        self.register_server_cmd(server_cmd)
        self.register_client_cmd(client_cmd)
        await self.registry.register(self.server_id, self.server_type)
        await self.broker.subscribe()
        self.add_timer(int(Config.ETCD_TTL / 2), self.registry.tick)

    async def start(self):
        await self.registry.watch_servers()

    async def exit(self):
        pass

    # 服务启动主要流程都在这里
    async def launch(self):
        #服务参数配置  组件的初始化
        await self.init()
        # 注册客户端与服务器rpc处理函数以及注册服务信息到etcd
        await self.register()
        # 启动前最后做一些逻辑操作，比如一些启用一些定时任务
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

    # 如果是直连客户端的服务器 第一个参数是client否者是player_id
    async def on_client_request(self, client, cmd, request):
        func = self.get_client_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(client, request)
            else:
                func(client, request)
        else:
            logging.error(f"no rpc func:{cmd}")

    def send_response_client(self, pid, pck):
        logging.info("由外部服务继承，并重写方法")

    # 如果是直连客户端的服务器 第一个参数是client否者是player_id
    # 如果是外部服务器 可以继承重写方法
    async def on_server_message(self, pid, cmd, pck):
        logging.info(f"on_server_message:pid:{pid}, cmd:{cmd}, pck:{pck}")
        # 查看是否是转发过来的客户端包 是的话由客户端来处理
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

    # 定时函数
    def add_timer(self, interval=60, func=None, *args, **kwargs):
        if func is None or self.exited:
            return

        async def decorated(*args, **kwargs):
            while True:
                await asyncio.sleep(interval, loop=self.loop)
                try:
                    if asyncio.iscoroutinefunction(func):
                        await func(*args, **kwargs)
                    else:
                        func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"timer func:{func} exec error e:{e}")
        self.loop.create_task(decorated())

    def get_report_info(self):
        info = {
            'ip': self.ip,
            'port': self.port,
        }
        return info

    def on_server_del(self, info):
        logging.info(f"on_server_del.info:{info} ")

    def on_server_add(self, info):
        logging.info(f"on_server_add.info:{info} ")

    # 一般为了节省内部流量 服务器内部消息头不加pid
    def send_server_message(self, server_type, server_id, pid, pck):
        cmd = pck.DESCRIPTOR.full_name
        data = BrokerPack().pack(pid, cmd, pck)
        logging.info(f"send server_type:{server_type}, server_id:{server_id}, pck:{pck}")
        if server_id == "*":
            self.loop.create_task(self.broker.send_to_group_server(server_type, data))
        elif server_id is not None and server_id != "":
            self.loop.create_task(self.broker.send_to_server(server_id, data))
        else:
            self.loop.create_task(self.broker.send_to_all_server(data))

    def send_response_by_gateway(self, pid, pck, sid="*"):
        self.send_server_message(SeverType.GATEWAY, sid, pid, pck)


# engine 实例
srv_inst: Engine = None
