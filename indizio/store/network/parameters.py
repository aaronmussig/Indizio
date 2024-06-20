from typing import List, Dict, Optional

import orjson
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.common.boolean import BooleanAllAny, BooleanShowHide
from indizio.models.network.parameters import NetworkFormLayoutOption, NetworkParamThreshold, NetworkParamDegree, \
    NetworkParamNodeColor, NetworkParamNodeSize, NetworkParamEdgeWeights


class NetworkFormStoreModel(BaseModel):
    """
    This class represents the data that is stored in the network form store.
    """

    layout: NetworkFormLayoutOption = NetworkFormLayoutOption.circle
    node_of_interest: List[str] = list()
    thresholds: Dict[str, NetworkParamThreshold] = dict()
    thresh_matching: BooleanAllAny = BooleanAllAny.ANY
    degree: NetworkParamDegree = NetworkParamDegree()
    show_edges_to_self: BooleanShowHide = BooleanShowHide.HIDE
    node_color: Optional[NetworkParamNodeColor] = None
    node_size: Optional[NetworkParamNodeSize] = None
    edge_weights: Optional[NetworkParamEdgeWeights] = None

    def get_focal_node_str(self):
        """Returns the string output of the focal node."""
        return ', '.join(self.node_of_interest) if self.node_of_interest else 'All'

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
            data=NetworkFormStoreModel().model_dump(mode='json')
        )
