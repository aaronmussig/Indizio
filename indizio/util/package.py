from importlib.resources import files
from pathlib import Path


def get_package_root() -> Path:
    """
    Returns the installation directory for the package.
    """
    return files('indizio')
