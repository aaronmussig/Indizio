import functools
import os
import tempfile
from pathlib import Path

import orjson
from diskcache import Cache
from frozendict import frozendict

from indizio.cache import CACHE
from indizio.util.hashing import calc_md5


def to_hashable(obj):
    """
    Serializes a nested dictionary to a frozendict for memoization.
    """
    if isinstance(obj, dict):
        return frozendict((k, to_hashable(v)) for k, v in obj.items())
    if isinstance(obj, list) or isinstance(obj, tuple):
        return tuple(to_hashable(x) for x in obj)
    return obj


def from_hashable(obj):
    """
    De-serializes a frozendict to a dictionary.
    """
    if isinstance(obj, frozendict):
        return {k: from_hashable(v) for k, v in obj.items()}
    if isinstance(obj, tuple):
        return [from_hashable(x) for x in obj]
    return obj


def freezeargs(func):
    """
    Wrapper to transform a function's arguments to a hashable type.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        print(args)
        print(kwargs)
        args_frozen = to_hashable(args)
        kwargs_frozen = to_hashable(kwargs)
        return func(*args_frozen, **kwargs_frozen)

    return wrapped


def get_tmp_dir() -> Path:
    """
    Returns a temporary path for storing files.
    This is set to be prefixed by the parent PID.
    """
    parent_pid = os.getppid()
    tmp_root = tempfile.gettempdir()
    return Path(tmp_root) / f'indizio-{parent_pid}'


def cache_by(kwargs_to_cache):
    """
    This wrapper will use the diskcache to memoize the function's results
    based on the keys given.
    """
    # If a string is provided, convert it into a list for consistency
    if isinstance(kwargs_to_cache, str):
        kwargs_to_cache = [kwargs_to_cache]

    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Generate the cache key
            cache_key = {
                'func': repr(func),
            }
            for key in kwargs_to_cache:
                cache_key[key] = kwargs[key]
            cache_key = orjson.dumps(cache_key, option=orjson.OPT_SORT_KEYS)
            cache_key = calc_md5(cache_key)

            print(f"kwargs_to_cache: {cache_key}")

            # Check the cache to see if the result already exists
            with Cache(CACHE.directory) as cache:
                existing_result = cache.get(cache_key)
                if existing_result:
                    print('found existing result')
                    return existing_result

            # Otherwise, run the function and save the result
            result = func(*args, **kwargs)
            print('result')
            with Cache(CACHE.directory) as cache:
                print('saving to cache')
                cache.set(cache_key, result)
                print('done saving')
            return result

        return wrapper

    return actual_decorator
