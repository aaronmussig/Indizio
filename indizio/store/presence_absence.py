from pathlib import Path
from typing import Optional, Dict

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.distance_matrix import DistanceMatrixFile
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df


class PresenceAbsenceFile(BaseModel):
    file_name: str
    file_id: str
    path: Path
    hash: str

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the uploaded file data to a presence/absence file.
        """
        df = pd.read_table(data.path, sep=',', dtype=str)
        df.set_index(df.columns[0], inplace=True)
        df = df.astype(float)
        path, md5 = to_pickle_df(df)
        return cls(file_name=data.file_name, file_id=data.name, path=path, hash=md5)

    def read(self) -> pd.DataFrame:
        """
        Return the saved P/A matrix from disk.
        """
        return from_pickle_df(self.path)

    def as_distance_matrix(self) -> DistanceMatrixFile:
        # Convert the dataframe to a distance matrix and compute the correlation
        df_corr = self.read().corr().abs()
        df_min = df_corr.min().min()
        df_max = df_corr.max().max()

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


class PresenceAbsenceStore(dcc.Store):
    ID = 'presence-absence-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
