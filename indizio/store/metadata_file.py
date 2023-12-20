import io
import json

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormStoreData


class MetadataFile(BaseModel):
    file_name: str
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_upload_data(cls, data: UploadFormStoreData):
        decoded_str = io.StringIO(data.data.decode('utf-8'))
        df = pd.read_table(decoded_str, sep=',', index_col=0)
        return cls(file_name=data.file_name, data=df)

    def serialize(self):
        return {'file_name': self.file_name, 'df': self.df.to_json()}

    @classmethod
    def deserialize(cls, data):
        return cls(file_name=data['file_name'], df=pd.read_json(io.StringIO(data['df'])))


class MetadataFileStore(dcc.Store):
    ID = 'metadata-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
