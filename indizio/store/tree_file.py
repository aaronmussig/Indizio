import io
import json

import dendropy
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormStoreData


class TreeFile(BaseModel):
    file_name: str
    tree: dendropy.Tree
    newick: str

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_upload_data(cls, data: UploadFormStoreData):
        decoded_str = io.StringIO(data.data.decode('utf-8'))
        tree = dendropy.Tree.get(data=decoded_str, schema='newick')
        return cls(file_name=data.file_name, newick=decoded_str, tree=tree)

    def serialize(self):
        return {'file_name': self.file_name, 'newick': self.newick}

    @classmethod
    def deserialize(cls, data):
        newick = data['newick']
        tree = dendropy.Tree.get(data=newick, schema='newick')
        return cls(file_name=data['file_name'], newick=newick, tree=tree)


class TreeFileStore(dcc.Store):
    ID = 'tree-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
