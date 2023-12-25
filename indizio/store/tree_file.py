from pathlib import Path
from typing import Optional, Dict

import dendropy
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.store.upload_form_store import UploadFormItem
from indizio.util.files import to_pickle, from_pickle


class TreeFile(BaseModel):
    file_name: str
    file_id: str
    path: Path
    hash: str

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the tree into a pickle.
        """
        tree = dendropy.Tree.get_from_path(data.path.as_posix(), schema='newick')
        path, md5 = to_pickle(tree)
        return cls(file_name=data.file_name, name=data.name, path=path, hash=md5)

    def read(self) -> dendropy.Tree:
        return from_pickle(self.path)

class TreeData(BaseModel):
    data: Dict[str, TreeFile] = dict()

    def add_item(self, item: TreeFile):
        self.data[item.file_id] = item

    def get_files(self):
        return self.data.values()

class TreeFileStore(dcc.Store):
    ID = 'tree-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
