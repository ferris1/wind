from aioetcd3.client import client
from engine.config.IpConfig import ETCD_ADDR
from engine.config import Config
import logging
import json
from aioetcd3.help import range_prefix
import asyncio
from aioetcd3.watch import Event, EVENT_TYPE_DELETE
from contextlib import suppress
import time

# use aioetcd3   https://github.com/gaopeiliang/aioetcd3

class EtcdRegistry:
    def __init__(self):
        self.aio_etcd = client(ETCD_ADDR)
        self.etcd_lease = None
        self.etcd_lease_ttl = Config.ETCD_TTL
        self.etcd_group = Config.ETCD_GROUP    # 确保一个etcd数据库可以服务多个服务器
        self.watch_types = set()
        self.online_servers = dict()
        self.watched_tasks = []
        self.srv_inst = None
        self.status = False
        self.last_etcd_tick_time = 0

    async def init(self, srv_inst):
        self.srv_inst = srv_inst
        try:
            await self.aio_etcd.status()
        except Exception as ex:
            logging.error("no etcd valid server")
            self.status = False
        else:
            self.status = True

    async def register(self, server_id, server_type):
        if not self.status:
            return
        self.etcd_lease = await self.aio_etcd.grant_lease(self.etcd_lease_ttl)
        node_key = self.get_type_key(self.srv_inst.server_type) + self.srv_inst.server_id
        info = self.srv_inst.get_report_info()
        if self.etcd_lease_ttl is not None and self.etcd_lease is not None:
            await self.aio_etcd.put(node_key, json.dumps(info), lease=self.etcd_lease)
            logging.info(f'update info in etcd {server_type} {server_id} {info}')
        else:
            logging.error(f"register_server etcd error")

    def get_server_by_type(self, server_type):
        lst = list(self.online_servers.get(server_type, {}).keys())
        return lst

    def get_type_key(self, server_type):
        return '/' + self.etcd_group + '/servers/' + str(server_type) + '/'

    def add_watches(self, type_lst):
        self.watch_types.update(type_lst)
        for server_type in self.watch_types:
            self.online_servers[server_type] = dict()

    async def watch_servers(self):
        if not self.status:
            return
        logging.info(f"start watch types:{self.watch_types}")
        for server_type in self.watch_types:
            wt = asyncio.create_task(self.watch_node(self.get_type_key(server_type)))
            self.watched_tasks.append(wt)
        for server_type in self.watch_types:
            await self.update_servers_by_type(server_type)

    async def watch_node(self, node):
        logging.info(f"start watch etcd node:{node}")
        async with self.aio_etcd.watch_scope(range_prefix(node), always_reconnect=True) as response:
            async for event in response:
                if event is None:
                    logging.info("watch_nodes success")
                    continue
                self.on_etcd_event(event)

    def on_etcd_event(self, event: Event):
        params = event.key.decode().split('/')
        server_type = int(params[-2])
        sid = params[-1]
        cur_servers = self.online_servers[server_type]
        info = cur_servers.get(sid)
        if event.type == EVENT_TYPE_DELETE:
            if info:
                cur_servers.pop(sid)
                self.on_server_del(info)
        else:
            value = event.value
            if value:
                new_info = json.loads(value.decode())
                new_info['sid'] = sid
                new_info['type'] = server_type
                cur_servers[sid] = new_info
                if info is None:
                    self.on_server_add(new_info)

    async def update_servers_by_type(self, server_type):
        old_servers = self.online_servers.get(server_type, dict())
        self.online_servers[server_type] = dict()
        lst = await self.aio_etcd.range(key_range=range_prefix(self.get_type_key(server_type)))
        for v in lst:
            sid = v[0].decode().split('/')[-1]
            # 自己的不算
            if sid == self.srv_inst.server_id:
                continue
            info = json.loads(v[1].decode())
            info['sid'] = sid
            info['type'] = server_type
            self.online_servers[server_type][sid] = info

        cur_servers = self.online_servers[server_type]
        for sid, info in old_servers.items():
            if sid not in cur_servers:
                self.on_server_del(info)
        for sid, info in cur_servers.items():
            if sid not in old_servers:
                self.on_server_add(info)
        logging.info(f"update servers by type:{server_type} cur_servers:{cur_servers}")
        return cur_servers

    def on_server_del(self, info):
        self.srv_inst.on_server_del(info)

    def on_server_add(self, info):
        self.srv_inst.on_server_add(info)

    # cancel的时候会报CancelledError错   这个错可以忽略
    # https://stackoverflow.com/questions/43804993/asyncio-cancellederror-and-keyboardinterrupt
    async def cancel_all_watch(self):
        for task in self.watched_tasks:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

    async def clean_etcd(self):
        try:
            await self.cancel_all_watch()
            node_key = self.get_type_key(self.srv_inst.server_type) + self.srv_inst.server_id
            await self.aio_etcd.delete(node_key)
            logging.info(f'delete key in etcd {node_key}')
            if self.etcd_lease:

                self.etcd_lease = None
        except Exception as e:
            logging.error(f'error when clean etcd: {e}')

    async def tick(self):
        logging.info(f"etcd tick,self.online_server:{self.online_servers}")
        if self.srv_inst.exited:
            return
        if self.etcd_lease_ttl is None:
            return
        try:
            if await self.aio_etcd.refresh_lease(self.etcd_lease):
                self.last_etcd_tick_time = time.time()
        except Exception as e:
            logging.error(f'etcd tick error: {e}')
        finally:
            if time.time() - self.last_etcd_tick_time > self.etcd_lease_ttl:
                logging.critical("server in etcd out of data ")

