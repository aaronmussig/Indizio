from pydantic import BaseModel

from indizio.models.common.bound import Bound
from indizio.models.common.html_option import HtmlOption


class EdgeWeights(HtmlOption):
    """
    This class is used to represent the options for showing edge weight in the graph.
    """

    HIDDEN = 'Hidden'
    TEXT = 'Text'
    WEIGHT = 'Line weight'
    BOTH = 'Text & Line Weight'


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


class NetworkParamNodeColor(BaseModel):
    file_id: str
    column: str


class NetworkParamNodeSize(BaseModel):
    file_id: str
    column: str


class NetworkParamEdgeWeights(BaseModel):
    file_id: str
    value: EdgeWeights = EdgeWeights.HIDDEN
