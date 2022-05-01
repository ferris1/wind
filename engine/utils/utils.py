import importlib
import logging
import inspect
import asyncio
import functools


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
                    assert sorted(spec.args) == sorted(['player_id', 'request'])
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(ensure_future_pack, cb)
                assert (f.__name__[8:] not in cmd_map.keys())
                cmd_map[f.__name__[8:]] = cb
    logging.info(f'Loading finish with {len(cmd_map)} methods')
    return cmd_map
