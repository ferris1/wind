import importlib
import logging
import inspect
import asyncio
import functools
import sys
_int_to_bytes = int.to_bytes
_int_from_bytes = int.from_bytes


def uint32_to_bytes(i):
    return _int_to_bytes(i, length=4, byteorder='little', signed=False)


def uint_from_bytes(i):
    return _int_from_bytes(i, byteorder='little', signed=False)


# 创建执行任务使用create_task
def create_async_task(co, *args, **kwargs):
    return asyncio.create_task(co(*args, **kwargs))


def load_all_handlers(handlers_mod):
    root = importlib.import_module(handlers_mod)
    client_cmd_map = {}
    logging.info(f'Load handler in {handlers_mod}')
    for modname in root.__handlers__:
        # 只注册以handler开头的
        if not modname.startswith("handler"):
            continue
        m = importlib.import_module(handlers_mod + '.' + modname)
        for k in dir(m):
            if k.startswith('Handler_'):
                f = getattr(m, k)
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(create_async_task, cb)
                assert (f.__name__[8:] not in client_cmd_map.keys())
                client_cmd_map[f.__name__[8:]] = cb
    sever_cmd_map = {}
    for modname in root.__shandlers__:
        # 只注册以s_handler开头的
        if not modname.startswith("s_handler"):
            continue
        m = importlib.import_module(handlers_mod + '.' + modname)
        for k in dir(m):
            if k.startswith('Handler_'):
                f = getattr(m, k)
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(create_async_task, cb)
                assert (f.__name__[8:] not in sever_cmd_map.keys())
                sever_cmd_map[f.__name__[8:]] = cb
    logging.info(f'Loaded client {len(client_cmd_map)} methods, sever {len(sever_cmd_map)} methods')
    return client_cmd_map, sever_cmd_map


def check_async_cb(cb):
    if asyncio.iscoroutinefunction(cb):
        return functools.partial(create_async_task, cb)
    else:
        return cb


def init_asyncio_loop_policy():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        import uvloop
    except ImportError:
        logging.error('uvloop is not available')
    else:
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
