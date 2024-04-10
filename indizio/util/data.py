import numpy as np


def is_numeric(value, nan_not_numeric=True) -> bool:
    """
    Returns True if the value is numeric and False otherwise.
    Note that this function will return False for NaN values.
    """
    try:
        val = float(value)
        if np.isnan(val) and nan_not_numeric:
            return False
        return True
    except ValueError:
        return False
