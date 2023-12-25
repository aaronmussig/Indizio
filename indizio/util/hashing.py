import hashlib


def calc_md5(data: bytes) -> str:
    """
    Calculate the MD5 checksum of the given data.
    """
    return hashlib.md5(data).hexdigest()

