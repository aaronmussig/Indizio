from typing import Dict, Tuple, Set

import numpy as np
import pandas as pd

from indizio.util.data import is_numeric, to_numeric


class MetadataColumn:
    MISSING_VALUE_DISCRETE = 'N/A'
    MISSING_VALUE_CONTINUOUS = np.nan
    MISSING_HEX = '#FFFFFF'

    def __init__(self, column: pd.Series):
        self.column = column

    def iter_discrete_values(self):
        for index, value in self.column.items():
            if pd.isna(value):
                yield self.MISSING_VALUE_DISCRETE
            else:
                yield str(value)

    def get_discrete_value(self, index: str):
        value = self.column[index]
        if pd.isna(value):
            return self.MISSING_VALUE_DISCRETE
        return str(value)

    def get_continuous_value(self, index: str):
        value = self.column[index]
        if pd.isna(value):
            return self.MISSING_VALUE_CONTINUOUS
        value_parsed = to_numeric(value)
        if value_parsed is None:
            return self.MISSING_VALUE_CONTINUOUS
        return value_parsed

    def unique_values(self) -> Set[str]:
        """
        Get the unique values, this is only used for discrete columns.
        nans are replaced with the string 'N/A'
        """
        out = set()
        for key, value in self.column.items():
            if pd.isna(value):
                out.add(self.MISSING_VALUE_DISCRETE)
            else:
                out.add(str(value))
        return out

    def get_value_to_idx(self) -> Dict[str, int]:
        """
        Return a dictionary mapping unique values to an index. Only for discrete values.
        """
        out = dict()
        for value in self.column.values:
            if pd.isna(value):
                parsed_value = self.MISSING_VALUE_DISCRETE
            else:
                parsed_value = str(value)
            if parsed_value not in out:
                out[parsed_value] = len(out)
        return out

    def is_discrete(self) -> bool:
        n_missing = 0
        n_discrete = 0
        n_continuous = 0
        for key, value in self.column.items():
            if pd.isna(value):
                n_missing += 1
            elif is_numeric(value):
                n_continuous += 1
            else:
                n_discrete += 1
        return n_discrete > n_continuous

    def get_min_max(self) -> Tuple[float, float]:
        min_value, max_value = None, None
        for value in self.column.values:
            if pd.isna(value):
                continue
            value_as_float = to_numeric(value)
            if value_as_float is not None:
                try:
                    if min_value is None or value_as_float < min_value:
                        min_value = value_as_float
                    if max_value is None or value_as_float > max_value:
                        max_value = value_as_float
                except ValueError:
                    pass
        if min_value is None or max_value is None:
            raise ValueError('No valid continuous values found in column.')
        return min_value, max_value
