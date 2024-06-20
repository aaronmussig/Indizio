from typing import Dict, List, Tuple

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.tree.tree_file import TreeFile


class TreeFileStoreModel(BaseModel):
    data: Dict[str, TreeFile] = dict()

    def add_item(self, item: TreeFile):
        self.data[item.file_id] = item

    def get_files(self) -> Tuple[TreeFile, ...]:
        return tuple(self.data.values())

    def get_file(self, file_id: str) -> TreeFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id})
        return out


class TreeFileStore(dcc.Store):
    """
    This class is used to represent the store for the tree files.
    """
    ID = 'tree-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=TreeFileStoreModel().model_dump(mode='json')
        )
