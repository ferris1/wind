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
    cmd_map = {}
    logging.info(f'Load handler in {handlers_mod}')
    for modname in root.__handlers__:
        m = importlib.import_module(handlers_mod + '.' + modname)
        for k in dir(m):
            if k.startswith('Handler_'):
                f = getattr(m, k)
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(create_async_task, cb)
                assert (f.__name__[8:] not in cmd_map.keys())
                cmd_map[f.__name__[8:]] = cb
    logging.info(f'Loading finish with {len(cmd_map)} methods')
    return cmd_map


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
