import logging
from engine.SrvEngine import Engine
from engine import SrvEngine
from engine.utils.Utils import load_all_handlers
from service.game.modules.game_player_mgr import GamePlayerModules
from engine.client.ClientMgr import ClientMgr
import asyncio
from engine.utils.Const import SeverType


class GameSrv(Engine):
    def __init__(self):
        super().__init__("GameSrv", SeverType.GAME.value)

    async def init(self):
        await super().init()
        self.registry.add_watches({SeverType.GAME.value})
        await ClientMgr().init(self.ip, self.port)

    async def register(self):
        await super(GameSrv, self).register()
        self.register_cmd(load_all_handlers('service.game.handlers'))

    async def start(self):
        await super(GameSrv, self).start()
        logging.info("start Game Srv")
        GamePlayerModules().test_singleton()
        GamePlayerModules().test_singleton()

    async def exit(self):
        await super(GameSrv, self).exit()
        logging.info("exit Game Srv")

    async def on_client_request(self, client, cmd, request):
        func = self.get_cmd(cmd)
        if func:
            if asyncio.iscoroutinefunction(func):
                await func(client=client, request=request)
            else:
                func(client=client, request=request)
        else:
            logging.error(f"no rpc func:{cmd}")


def run():
    srv_inst = GameSrv()
    SrvEngine.srv_inst = srv_inst
    srv_inst.serve()


if __name__ == '__main__':
    run()

