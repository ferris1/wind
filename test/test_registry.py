from aioetcd3.client import client
from engine.config.IpConfig import ETCD_ADDR
from engine.config.Config import ETCD_GROUP
import json

import asyncio


async def test_add():
    key = '/' + ETCD_GROUP + '/servers/' + '1' + '/'

    c = client(ETCD_ADDR)

    info = {
        'ip': "127.0.0.1",
        'port': 5050,
    }
    print("put hello1")
    await c.put(key + "hello1", json.dumps(info))
    print("put hello2")
    await c.put(key + "hello2", json.dumps(info))
    print("put hello3")
    await c.put(key + "hello3", json.dumps(info))


async def test_delete():
    key = '/' + ETCD_GROUP + '/servers/' + '1' + '/'
    await asyncio.sleep(5)
    c = client(ETCD_ADDR)
    print("put hello1")
    await c.delete(key + "hello1")
    print("put hello2")
    await c.delete(key + "hello2")
    print("put hello3")
    await c.delete(key + "hello3")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.create_task()
    f1 = loop.create_task(test_add())
    f2 = loop.create_task(test_delete())
    loop.run_until_complete(asyncio.gather(f1, f2))
