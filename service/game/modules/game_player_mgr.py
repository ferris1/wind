from engine.utils.Singleton import Singleton
import logging


class GamePlayerModules(Singleton):
    def __init__(self):
        pass

    def test_singleton(self):
        logging.info(f"id:{id(self)}")
