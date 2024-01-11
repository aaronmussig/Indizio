from pathlib import Path
from typing import Dict, List

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.distance_matrix import DistanceMatrixFile
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df, get_delimiter


class PresenceAbsenceFile(BaseModel):
    file_name: str
    file_id: str
    path: Path
    hash: str
    n_cols: int
    n_rows: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the uploaded file data to a presence/absence file.
        """
        delimiter = get_delimiter(data.path)
        df = pd.read_table(data.path, sep=delimiter, dtype=str)
        df.set_index(df.columns[0], inplace=True)
        df = df.astype(float)
        path, md5 = to_pickle_df(df)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            n_cols=int(df.shape[1]),
            n_rows=int(df.shape[0])
        )

    def read(self) -> pd.DataFrame:
        """
        Return the saved P/A matrix from disk.
        """
        return from_pickle_df(self.path)

    def as_distance_matrix(self) -> DistanceMatrixFile:
        # Convert the dataframe to a distance matrix and compute the correlation
        df_corr = self.read().corr().abs()
        df_min = float(df_corr.min().min())
        df_max = float(df_corr.max().max())

        # Store the correlation matrix on disk
        path, md5 = to_pickle_df(df_corr)

        # Create the distance matrix
        return DistanceMatrixFile(
            file_name=self.file_name,
            file_id=f'{self.file_id if self.file_id else self.file_name} (Pearson Corr.)',
            path=path,
            hash=md5,
            min_value=df_min,
            max_value=df_max,
            n_cols=int(df_corr.shape[1]),
            n_rows=int(df_corr.shape[0])
        )


class PresenceAbsenceData(BaseModel):
    """
    This class represents the presence absence store.
    Items are keyed by their hash.
    """
    data: Dict[str, PresenceAbsenceFile] = dict()

    def add_item(self, item: PresenceAbsenceFile):
        """
        Add an item to the store.
        """
        self.data[item.file_id] = item

    def get_files(self):
        return self.data.values()

    def get_file(self, file_id: str) -> PresenceAbsenceFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id})
        return out


class PresenceAbsenceStore(dcc.Store):
    ID = 'presence-absence-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
