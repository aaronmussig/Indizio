import csv
import io
import pickle
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from indizio.config import TMP_DIR
from indizio.util.hashing import calc_md5


def to_pickle_df(df: pd.DataFrame) -> Tuple[Path, str]:
    """
    Save a dataframe to a pickle object.
    Returns the temp path to the pickle object (by default, this is the md5).
    """
    # Save the dataframe to a buffer
    buffer = io.BytesIO()
    df.to_pickle(buffer)
    value = buffer.getvalue()

    # Compute the path based on the md5
    md5 = calc_md5(value)
    path = TMP_DIR / md5

    # Write to disk
    with open(path, 'wb') as f:
        f.write(value)
    return path, md5


def from_pickle_df(path: Path) -> pd.DataFrame:
    """
    Read a Pandas dataframe pickle from disk.
    """
    with open(path, 'rb') as f:
        return pd.read_pickle(f)


def to_pickle(obj) -> Tuple[Path, str]:
    """
    Save a dataframe to a pickle object.
    Returns the temp path to the pickle object (by default, this is the md5).
    """
    buffer = io.BytesIO()
    pickle.dump(obj, buffer, protocol=pickle.HIGHEST_PROTOCOL)
    value = buffer.getvalue()

    # Compute the path based on the md5
    md5 = calc_md5(value)
    path = TMP_DIR / md5

    # Write to disk
    with open(path, 'wb') as f:
        f.write(value)

    return path, md5


def from_pickle(path: Path):
    """
    Load a pickle object from disk.
    """
    with open(path, 'rb') as f:
        return pickle.load(f)


def to_file(data: bytes, name: Optional[str] = None) -> Path:
    """
    Saves the bytes object to disk and returns the path.
    """
    if name is None:
        name = calc_md5(data)
    path = TMP_DIR / name
    with open(path, 'wb') as f:
        f.write(data)
    return path


def get_delimiter(file_path: Path, n_lines=5):
    """
    Automatic detection of a delimiter used in a file.
    """
    sniffer = csv.Sniffer()
    lines = list()
    with file_path.open() as f:
        for _ in range(n_lines):
            lines.append(f.readline())
    sample = '\n'.join(lines)
    return sniffer.sniff(sample).delimiter
