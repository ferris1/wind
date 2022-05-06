import logging
from engine.SrvEngine import Engine
from engine import SrvEngine
from engine.utils.Utils import load_all_handlers
from engine.client.ClientMgr import ClientMgr
from engine.utils.Const import SeverType
from service.gateway.mgrs.gate_router_mgr import GateRouterMgr
import asyncio

class GatewaySrv(Engine):
    def __init__(self):
        super().__init__("GatewaySrv", SeverType.GATEWAY)

    async def init(self):
        await super().init()
        self.registry.add_watches({SeverType.GAME,SeverType.GATEWAY})
        await ClientMgr().init(self.ip, self.port)

    async def register(self):
        await super(GatewaySrv, self).register()
        self.register_client_cmd(load_all_handlers('service.gateway.handlers_client'))
        self.register_server_cmd(load_all_handlers('service.gateway.handlers_server'))

    async def on_client_request(self, client, cmd, request):
        logging.info(f"on_client_request cmd:{cmd} ")
        server_type = GateRouterMgr().get_cmd_router_server(cmd)
        if server_type:  # 如果是路由消息  直接转发服务器消息给对应服务器
            logging.info(f"router request to server_type:{server_type}")
            await self.send_server_message(server_type, "*", client.player_id, request)
        else:
            await super(GatewaySrv, self).on_client_request(client, cmd, request)

    async def on_server_message(self, pid, cmd, pck):
        logging.info(f"on_server_message:pid:{pid}, cmd:{cmd}, pck:{pck}")
        func = self.get_server_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(pid, pck)
            else:
                func(pid, pck)
        else:  # 如果没有的话  直接发给客户端
            client = ClientMgr().get_client_by_player_id(pid)
            client.send_packet(pck)
            logging.info(f"send_packet pck:{pck}")

    async def start(self):
        await super(GatewaySrv, self).start()
        logging.info("start GatewaySrv")

    async def exit(self):
        await super(GatewaySrv, self).exit()
        logging.info("exit GatewaySrv")


def run():
    srv_inst = GatewaySrv()
    SrvEngine.srv_inst = srv_inst
    srv_inst.serve()


if __name__ == '__main__':
    run()

