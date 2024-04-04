from pathlib import Path
from importlib.resources import files


def get_package_root() -> Path:
    return files('indizio')

