from typing import List, Optional, Dict

from pydantic import BaseModel


class LegendItem(BaseModel):
    """
    This class is used to store the data for a key in a legend group.
    """
    text: Optional[str] = None  # only for discrete
    hex_code: str


class LegendGroup(BaseModel):
    name: str  # i.e. a column name in the metadata file

    discrete_bins: Dict[str, LegendItem] = dict()

    continuous_bins: List[float] = list()
    continuous_colorscale: Optional[str] = None

    def is_discrete(self) -> bool:
        return len(self.discrete_bins) > 0

    def is_continuous(self) -> bool:
        return len(self.continuous_bins) > 0

    def set_discrete_group_hex(self, name: str, color: str):
        self.discrete_bins[name].hex_code = color

    def set_continuous_group_bins(self, bins: List[float]):
        self.continuous_bins = bins

    def set_continuous_group_colorscale(self, colorscale: str):
        self.continuous_colorscale = colorscale

    def get_discrete_key_to_hex(self) -> Dict[str, str]:
        return {key: value.hex_code for key, value in self.discrete_bins.items()}