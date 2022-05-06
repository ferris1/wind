import logging
from engine.SrvEngine import Engine
from engine import SrvEngine
from engine.utils.Utils import load_all_handlers
from engine.client.ClientMgr import ClientMgr
from engine.utils.Const import SeverType


class GatewaySrv(Engine):
    def __init__(self):
        super().__init__("GameSrv", SeverType.GAME)

    async def init(self):
        await super().init()
        self.registry.add_watches({SeverType.GAME})
        await ClientMgr().init(self.ip, self.port)

    async def register(self):
        await super(GatewaySrv, self).register()
        self.register_client_cmd(load_all_handlers('service.game.handlers_client'))
        self.register_server_cmd(load_all_handlers('service.game.handlers_server'))

    async def start(self):
        await super(GatewaySrv, self).start()
        logging.info("start Game Srv")

    async def exit(self):
        await super(GatewaySrv, self).exit()
        logging.info("exit Game Srv")


def run():
    srv_inst = GatewaySrv()
    SrvEngine.srv_inst = srv_inst
    srv_inst.serve()


if __name__ == '__main__':
    run()

