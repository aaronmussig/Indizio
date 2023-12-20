import io

import pandas as pd
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.distance_matrix import DistanceMatrixFile
from indizio.store.upload_form_store import UploadFormStoreData


class PresenceAbsenceFile(BaseModel):
    file_name: str
    df: pd.DataFrame

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_upload_data(cls, data: UploadFormStoreData):
        decoded_str = io.StringIO(data.data.decode('utf-8'))
        df = pd.read_table(decoded_str, sep=',', dtype=str)
        df.set_index(df.columns[0], inplace=True)
        df = df.astype(float)
        return cls(file_name=data.file_name, df=df)

    def as_distance_matrix(self) -> DistanceMatrixFile:
        return DistanceMatrixFile(file_name=self.file_name, df=self.df.corr().abs())

    def serialize(self):
        return {'file_name': self.file_name, 'df': self.df.to_json()}

    @classmethod
    def deserialize(cls, data):
        return cls(file_name=data['file_name'], df=pd.read_json(io.StringIO(data['df'])))


class PresenceAbsenceFileStore(dcc.Store):
    ID = 'presence-absence-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
