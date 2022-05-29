import logging
from engine.SrvEngine import Engine
from engine import SrvEngine
from engine.utils.Utils import load_all_handlers
from engine.client.ClientMgr import ClientMgr
from engine.utils.Const import SeverType


class GameSrv(Engine):
    def __init__(self):
        super().__init__("GameSrv", SeverType.GAME)

    async def init(self):
        await super().init()
        self.registry.add_watches({SeverType.GAME,SeverType.GATEWAY})

    async def register(self):
        await super(GameSrv, self).register()
        client_cmd, server_cmd = load_all_handlers('service.game.handlers')
        self.register_server_cmd(server_cmd)
        self.register_client_cmd(client_cmd)

    async def start(self):
        await super(GameSrv, self).start()

        logging.info("start Game Srv")

    async def exit(self):
        await super(GameSrv, self).exit()
        logging.info("exit Game Srv")


def run():
    srv_inst = GameSrv()
    SrvEngine.srv_inst = srv_inst
    srv_inst.serve()


if __name__ == '__main__':
    run()

