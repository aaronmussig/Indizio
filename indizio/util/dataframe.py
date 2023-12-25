import pandas as pd

import numpy as np


def dataframe_to_pairs(df: pd.DataFrame):
    """Extracts the pairs of values from the upper triangle of a dataframe."""
    return df.where(np.triu(np.ones(df.shape)).astype(bool)).stack()
