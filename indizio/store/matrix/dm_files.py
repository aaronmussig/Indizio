from typing import Dict, Tuple, List

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.distance_matrix.dm_file import DistanceMatrixFile


class DistanceMatrixStoreModel(BaseModel):
    """
    This class is the actual model for the data in the distance matrix store.
    """
    data: Dict[str, DistanceMatrixFile] = dict()

    def add_item(self, item: DistanceMatrixFile):
        self.data[item.file_id] = item

    def get_files(self) -> Tuple[DistanceMatrixFile, ...]:
        return tuple(self.data.values())

    def get_file(self, file_id: str) -> DistanceMatrixFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id, })
        return out


class DistanceMatrixStore(dcc.Store):
    """
    This class is used to represent the store for the distance matrix files.
    """

    ID = 'distance-matrix-file-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=DistanceMatrixStoreModel().model_dump(mode='json')
        )
