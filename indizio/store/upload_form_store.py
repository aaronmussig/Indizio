
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE


class UploadFormStoreData(BaseModel):
    """
    This class represents the data that is stored in the network form store.
    """
    file_name: str
    data: bytes


class UploadFormStore(dcc.Store):
    ID = 'upload-form-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=list()
        )
