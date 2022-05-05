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


def ensure_future_pack(co, *args, **kwargs):
    return asyncio.ensure_future(co(*args, **kwargs))


def load_all_handlers(hanglers_mod):
    root = importlib.import_module(hanglers_mod)
    cmd_map = {}
    logging.info(f'Load handler in {hanglers_mod}')
    for modname in root.__handlers__:
        m = importlib.import_module(hanglers_mod + '.' + modname)
        for k in dir(m):
            if k.startswith('Handler_'):
                f = getattr(m, k)
                spec = inspect.getfullargspec(f)
                if hanglers_mod == 'game.handlers':
                    assert sorted(spec.args) == sorted(['rpc_client', 'request'])
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(ensure_future_pack, cb)
                assert (f.__name__[8:] not in cmd_map.keys())
                cmd_map[f.__name__[8:]] = cb
    logging.info(f'Loading finish with {len(cmd_map)} methods, cmd_map:{cmd_map}')
    return cmd_map


def asyncio_ensure_future(co, *args, **kwargs):
    return asyncio.ensure_future(co(*args, **kwargs))


def check_async_cb(cb):
    if asyncio.iscoroutinefunction(cb):
        return functools.partial(asyncio_ensure_future, cb)
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
