from pathlib import Path
from typing import Tuple

import pandas as pd
from pydantic import BaseModel

from indizio.models.upload.upload_file import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df, get_delimiter


class DistanceMatrixFile(BaseModel):
    """
    This class is used to represent a single distance matrix that has been uploaded.
    """
    file_name: str
    file_id: str
    path: Path
    hash: str
    min_value: float
    max_value: float
    n_cols: int
    n_rows: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the data from the upload form store into a distance matrix file
        """
        delimiter = get_delimiter(data.path)
        df = pd.read_table(data.path, sep=delimiter, index_col=0)
        min_value = float(df.min().min())
        max_value = float(df.max().max())
        path, md5 = to_pickle_df(df)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            min_value=min_value,
            max_value=max_value,
            n_cols=int(df.shape[1]),
            n_rows=int(df.shape[0])
        )

    def read(self) -> pd.DataFrame:
        """
        Read the distance matrix from disk.
        """
        return from_pickle_df(self.path)

    def get_min_max(self) -> Tuple[float, float]:
        """
        Obtain the minimum and maximum values from the distance matrix.
        """
        df = self.read()
        return float(df.min().min()), float(df.max().max())
