from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
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


class NetworkFormStoreData(BaseModel):
    """
    This class represents the data that is stored in the network form store.
    """

    layout: NetworkFormLayoutOption = NetworkFormLayoutOption.grid
    node_of_interest: list[str] = list()
    thresh_degree: int = 0
    thresh_corr_select: NetworkThreshCorrOption = NetworkThreshCorrOption.GEQ
    corr_input: float = 0.0
    is_set: bool = False


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
