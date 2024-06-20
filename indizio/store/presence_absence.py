from typing import Dict, List, Tuple

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.presence_absence.pa_file import PresenceAbsenceFile


class PresenceAbsenceStoreModel(BaseModel):
    """
    This class represents the presence absence store.
    Items are keyed by their hash.
    """
    data: Dict[str, PresenceAbsenceFile] = dict()

    def add_item(self, item: PresenceAbsenceFile):
        """
        Add an item to the store.
        """
        self.data[item.file_id] = item

    def get_files(self) -> Tuple[PresenceAbsenceFile, ...]:
        return tuple(self.data.values())

    def get_file(self, file_id: str) -> PresenceAbsenceFile:
        return self.data[file_id]

    def as_options(self) -> List[Dict[str, str]]:
        """Returns the keys of the data as a dictionary of HTML options"""
        out = list()
        for file in self.get_files():
            out.append({'label': file.file_id, 'value': file.file_id})
        return out


class PresenceAbsenceStore(dcc.Store):
    """
    This class is used to represent the store for the presence absence files.
    """
    ID = 'presence-absence-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=PresenceAbsenceStoreModel().model_dump(mode='json')
        )
