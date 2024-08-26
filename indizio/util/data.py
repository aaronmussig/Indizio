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


def normalize(values, min_value=0, max_value=1):
    """Normalize a list of values to be within a specified range."""
    min_val = min(values)
    max_val = max(values)
    return [(max_value - min_value) * (val - min_val) / (max_val - min_val) + min_value for val in values]
