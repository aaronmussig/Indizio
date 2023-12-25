from pathlib import Path
from typing import Optional, Dict

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df


class MetadataFile(BaseModel):
    file_name: str
    file_id: Optional[str] = None
    path: Path
    hash: str

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Create a metadata file from the upload data.
        """
        df = pd.read_table(data.path, sep=',', index_col=0)
        path, md5 = to_pickle_df(df)
        return cls(file_name=data.file_name, file_id=data.name, path=path, hash=md5)

    def read(self) -> pd.DataFrame:
        return from_pickle_df(self.path)


class MetadataData(BaseModel):
    data: Dict[str, MetadataFile] = dict()

    def add_item(self, item: MetadataFile):
        self.data[item.file_id] = item

    def get_files(self):
        return self.data.values()


class MetadataFileStore(dcc.Store):
    ID = 'metadata-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
