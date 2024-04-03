import numpy as np

def is_numeric(value) -> bool:
    try:
        val = float(value)
        if np.isnan(val):
            return False
        return True
    except ValueError:
        return False
