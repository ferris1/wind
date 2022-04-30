import logging
from engine.SrvEngine import Engine
from engine import SrvEngine


class GameSrv(Engine):
    def __init__(self):
        super().__init__("GameSrv")

    async def init(self):
        await super().init()

    async def register(self):
        await super(GameSrv, self).register()

    async def start(self):
        await super(GameSrv, self).start()
        logging.info("start Game Srv")

    async def exit(self):
        await super(GameSrv, self).exit()
        logging.info("exit Game Srv")


def run():
    srv_inst = GameSrv()
    SrvEngine.set_srv_instance(srv_inst)
    srv_inst.run()


if __name__ == '__main__':
    run()

