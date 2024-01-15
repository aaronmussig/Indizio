from pathlib import Path
from typing import Dict, List

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
    n_leaves: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the tree into a pickle.
        """
        tree = dendropy.Tree.get_from_path(data.path.as_posix(), schema='newick')
        path, md5 = to_pickle(tree)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            n_leaves=len(tree.taxon_namespace)
        )

    def read(self) -> dendropy.Tree:
        return from_pickle(self.path)


class TreeData(BaseModel):
    data: Dict[str, TreeFile] = dict()

    def add_item(self, item: TreeFile):
        self.data[item.file_id] = item

    def get_files(self):
        return tuple(self.data.values())

    def get_file(self, file_id: str):
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id})
        return out


class TreeFileStore(dcc.Store):
    ID = 'tree-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
