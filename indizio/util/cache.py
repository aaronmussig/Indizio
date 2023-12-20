import functools

from frozendict import frozendict


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
