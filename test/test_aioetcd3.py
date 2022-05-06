
from aioetcd3.client import client
from engine.config.IpConfig import ETCD_ADDRS
from aioetcd3.help import range_prefix
from aioetcd3.watch import EVENT_TYPE_CREATE,EVENT_TYPE_DELETE,EVENT_TYPE_MODIFY
import asyncio
from contextlib import suppress


async def test_watch():
    c = client(ETCD_ADDRS)
    print("test_watch")
    async with c.watch_scope(range_prefix('/foo/')) as response:
        async for event in response:
            if event is None:
                print("create_event done")
                continue
            if event.type == EVENT_TYPE_CREATE:
                print(" EVENT_TYPE_CREATE")
            elif event.type == EVENT_TYPE_DELETE:
                print(" EVENT_TYPE_DELETE")
            else:
                print(" EVENT_TYPE_MODIFY")
    print("end test_watch")


async def test_create():
    c = client(ETCD_ADDRS)
    print("test_create")
    for i in range(30):
        key = f"/foo/{i}"
        await c.put(key, "hello")
        print(f"put:{key}")
        await asyncio.sleep(1)


async def test_cancel(w):
    print("test_cancel")
    await asyncio.sleep(5)
    print("start cancel")
    # cancel 会引发 CancelledError
    w.cancel()
    with suppress(asyncio.CancelledError):
        await w


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    w = loop.create_task(test_watch())
    loop.create_task(test_create())
    loop.create_task(test_cancel(w))
    loop.run_forever()


