from pathlib import Path
from typing import Optional, Dict, List

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df, get_delimiter


class MetadataFile(BaseModel):
    file_name: str
    file_id: Optional[str] = None
    path: Path
    hash: str
    n_cols: int
    n_rows: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Create a metadata file from the upload data.
        """
        delimiter = get_delimiter(data.path)
        df = pd.read_table(data.path, sep=delimiter, index_col=0)
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
        return from_pickle_df(self.path)


class MetadataData(BaseModel):
    data: Dict[str, MetadataFile] = dict()

    def add_item(self, item: MetadataFile):
        self.data[item.file_id] = item

    def get_files(self):
        return tuple(self.data.values())

    def get_file(self, file_id: str) -> MetadataFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id })
        return out


class MetadataFileStore(dcc.Store):
    ID = 'metadata-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
