from pathlib import Path
from typing import Optional, Dict, List, Tuple

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df, get_delimiter


class MetadataFile(BaseModel):
    """
    This class is used to represent a single metadata file that has been uploaded.
    """
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
        df = pd.read_table(data.path, sep=delimiter, index_col=0, encoding='latin-1')
        path, md5 = to_pickle_df(df)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            n_cols=int(df.shape[1]),
            n_rows=int(df.shape[0])
        )

    def get_cols_as_html_options(self) -> List[Dict[str, str]]:
        out = list()
        df = self.read()
        for col in df.columns:
            out.append(dict(
                label=col,
                value=col
            ))
        return out

    def read(self) -> pd.DataFrame:
        return from_pickle_df(self.path)


class MetadataData(BaseModel):
    """
    This class is used to represent a collection of metadata files.
    """
    data: Dict[str, MetadataFile] = dict()

    def add_item(self, item: MetadataFile):
        self.data[item.file_id] = item

    def get_files(self) -> Tuple[MetadataFile]:
        return tuple(self.data.values())

    def get_file(self, file_id: str) -> MetadataFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id})
        return out


class MetadataFileStore(dcc.Store):
    """
    This class is used to represent the store for the metadata files.
    """

    ID = 'metadata-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
