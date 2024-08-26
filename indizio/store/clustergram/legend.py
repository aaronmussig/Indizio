from typing import Dict

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.clustergram.legend import LegendGroup


class ClustergramLegendStoreModel(BaseModel):
    """
    This class is the actual model for the data in the clustergram parameters.
    """
    groups: Dict[str, LegendGroup] = dict()

    def set_discrete_group_hex(self, group_name: str, key: str, color: str):
        self.groups[group_name].set_discrete_group_hex(key, color)

    def set_continuous_group_bins(self, group_name: str, bins: list):
        self.groups[group_name].set_continuous_group_bins(bins)

    def set_continuous_group_colorscale(self, group_name: str, colorscale: str):
        self.groups[group_name].set_continuous_group_colorscale(colorscale)

    def is_empty(self) -> bool:
        return len(self.groups) == 0

class ClustergramLegendStore(dcc.Store):
    """
    This class is used to represent the store for the clustergram parameters.
    """

    ID = 'clustergram-legend-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=ClustergramLegendStoreModel().model_dump(mode='json')
        )
