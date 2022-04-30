import importlib
import logging
import inspect
import asyncio
import functools


def ensure_future_pack(co, *args, **kwargs):
    return asyncio.ensure_future(co(*args, **kwargs))


def load_all_handlers(root_mod_name):
    root = importlib.import_module(root_mod_name)
    cmd_map = {}
    logging.info(f'Load handler in {root_mod_name}')
    for modname in root.__handlers__:
        m = importlib.import_module(root_mod_name + '.' + modname)
        for k in dir(m):
            if k.startswith('Handler_'):
                f = getattr(m, k)
                spec = inspect.getfullargspec(f)
                if root_mod_name == 'game.handlers':
                    assert sorted(spec.args) == sorted(['player_id', 'request'])
                assert k not in cmd_map.keys()
                cb = f
                if asyncio.iscoroutinefunction(f):
                    cb = functools.partial(ensure_future_pack, cb)
                cmd_map[f.__name__[8:]] = cb
    logging.info(f'Loading finish with {len(cmd_map)} methods')
    return cmd_map
