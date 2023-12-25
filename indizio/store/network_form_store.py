from typing import Optional, List, Dict

from dash import dcc
from pydantic import BaseModel
import orjson
from indizio.config import PERSISTENCE_TYPE
from indizio.interfaces.boolean import BooleanAllAny, BooleanShowHide
from indizio.interfaces.bound import  Bound
from indizio.interfaces.html_option import HtmlOption


class NetworkThreshCorrOption(HtmlOption):
    """This class represents the different threshold correlation options."""
    LT = '<'
    LEQ = '<='
    EQ = '='
    GT = '>'
    GEQ = '>='


class NetworkFormLayoutOption(HtmlOption):
    """
    This class represents the different layout options for the network graph.
    """
    grid = 'Grid'
    random = 'Random'
    circle = 'Circle'
    concentric = 'Concentric'
    breadthfirst = 'Breadthfirst'
    cose = 'Cose'
    cose_bilkent = 'Cose-bilkent'
    cola = 'Cola'
    klay = 'Klay'
    spread = 'Spread'
    euler = 'Euler'

class NetworkParamThreshold(BaseModel):
    file_id: str
    left_bound: Bound = Bound.INCLUSIVE
    right_bound: Bound = Bound.INCLUSIVE
    left_value: float
    right_value: float

class NetworkParamDegree(BaseModel):
    min_value: float = 0.0
    max_value: float = 1.0


class NetworkFormStoreData(BaseModel):
    """
    This class represents the data that is stored in the network form store.
    """

    layout: NetworkFormLayoutOption = NetworkFormLayoutOption.grid
    node_of_interest: List[str] = list()
    thresholds: Dict[str, NetworkParamThreshold] = dict()
    thresh_matching: BooleanAllAny = BooleanAllAny.ALL
    degree: NetworkParamDegree = NetworkParamDegree()
    show_edges_to_self: BooleanShowHide = BooleanShowHide.SHOW

    def get_focal_node_str(self):
        """Returns the string output of the focal node."""
        return ', '.join(self.node_of_interest) if self.node_of_interest else 'All'

    def get_threshold_str(self):
        """Returns the string output of the threshold filtering."""
        return 'TODO'

    def get_cache_key(self) -> bytes:
        """
        Returns a unique key for this object.
        Note that only the attributes that would affect the structure of the
        graph are considered.
        """
        param_json = self.model_dump(mode='json')
        param_json.pop('layout')
        return orjson.dumps(param_json, option=orjson.OPT_SORT_KEYS)


class NetworkFormStore(dcc.Store):
    """
    This class stores the options that have been selected in the network form,
    i.e. the parameters that control how the d3 network graph appears.
    """

    # Unique identifier that represents this component.
    ID = 'network-form-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=NetworkFormStoreData().model_dump(mode='json')
        )
