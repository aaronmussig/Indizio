from pathlib import Path
from typing import Optional, Dict

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE


class UploadFormItem(BaseModel):
    """
    This class represents the data that is stored in the upload form store.
    """
    file_name: str
    name: Optional[str] = None
    path: Path
    hash: str


class UploadFormData(BaseModel):
    """
    This class represents the upload form store.
    Items are keyed by their hash.
    """
    data: Dict[str, UploadFormItem] = dict()

    def add_item(self, item: UploadFormItem):
        """
        Adds an item to the store.
        """
        self.data[item.hash] = item

    def remove_item(self, file_hash: str):
        """
        Removes an item from the store.
        """
        self.data.pop(file_hash, None)


class UploadFormStore(dcc.Store):
    """
    This class is used to represent the store for the upload form.
    """
    ID = 'upload-form-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=dict()
        )
