import logging
from engine.SrvEngine import Engine
from engine import SrvEngine
from engine.utils.Utils import load_all_handlers
from engine.client.ClientMgr import ClientMgr
from engine.utils.Const import SeverType
from service.gateway.mgrs.gate_router_mgr import GateRouterMgr
import asyncio
from engine.utils.Const import MessageType, GET_MESSAGE_TYPE


class GatewaySrv(Engine):
    def __init__(self):
        super().__init__("GatewaySrv", SeverType.GATEWAY)

    async def init(self):
        await super().init()
        self.registry.add_watches({SeverType.GAME, SeverType.GATEWAY})
        await ClientMgr().init(self.ip, self.port)
        self.is_external = True

    async def register(self):
        await super(GatewaySrv, self).register()
        client_cmd, server_cmd = load_all_handlers('service.gateway.handlers')
        self.register_server_cmd(server_cmd)
        self.register_client_cmd(client_cmd)

    async def on_client_request(self, client, cmd, request):
        # logging.info(f"on_client_request cmd:{cmd} ")
        server_type = GateRouterMgr().get_cmd_router_server(cmd)
        if server_type != self.server_type:  # 如果是路由消息  直接转发服务器消息给对应服务器
            srv_id = GateRouterMgr().get_player_bind_server(client.player_id)
            self.send_server_message(server_type, srv_id, client.player_id, request)
        else:
            await super(GatewaySrv, self).on_client_request(client, cmd, request)

    def on_client_disconect(self, player_id):
        GateRouterMgr().on_player_leave(player_id)

    def send_response_client(self, pid, pck):
        if not self.is_external:
            logging.error("not external, can not send response to client")
            return
        # logging.info(f"send_response_client.pid:{pid} pck:{pck}")
        client = ClientMgr().get_client_by_player_id(pid)
        client.send_packet(pck)

    async def on_server_message(self, pid, cmd, pck):
        # 如果是路由过来的Response包的话  直接发给客户端
        if GET_MESSAGE_TYPE(cmd) == MessageType.PlayerResponse:
            self.send_response_client(pid, pck)
            return
        # logging.info(f"on_server_message:pid:{pid}, cmd:{cmd}, pck:{pck}")
        func = self.get_server_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(pid, pck)
            else:
                func(pid, pck)
        else:
            logging.info(f"no cmd:{cmd}")

    async def start(self):
        await super(GatewaySrv, self).start()
        # 每三秒检测一次心跳是否超时
        self.add_timer(3, ClientMgr().update)
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

