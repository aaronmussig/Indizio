import importlib.metadata

__name__ = 'indizio'

try:
    __version__ = importlib.metadata.version('indizio')
except importlib.metadata.PackageNotFoundError:
    __version__ = 'UNKNOWN'
