
import random
# 负载均衡组件  目前支持随机算法,未来支持最小阈值与最大阈值


class Selector:
    def __init__(self):
        self.registry = None

    def init(self, registry):
        self.registry = registry

    def random_choose(self, server_type):
        svr_list = self.registry.get_server_by_type(server_type)
        if len(svr_list) <= 0:
            return svr_list
        return random.choice(svr_list)

