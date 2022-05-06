from engine.utils.Singleton import Singleton
from engine.utils.Const import SeverType

server_router_dict = {
    SeverType.GAME: ["CreateRoleRequest"]
}


class GateRouterMgr(Singleton):
    def __init__(self):
        self.cmd_router_dict = {}
        self.load_router()

    def load_router(self):
        for typ, lst in server_router_dict.items():
            for proto_name in lst:
                self.cmd_router_dict[proto_name] = typ

    def get_cmd_router_server(self, cmd):
        return self.cmd_router_dict.get(cmd, SeverType.NONE)
