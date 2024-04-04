from typing import Optional, List

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.interfaces.html_option import HtmlOption


class MatrixBinOption(HtmlOption):
    """
    These are the select options provided when a user uploads a file.
    """
    CONTINUOUS = 'Continuous'
    BINNED = 'Binned'


class MatrixParameters(BaseModel):
    """
    This class is the actual model for the data in the matrix parameters.
    """
    metric: Optional[str] = None
    color_scale: str = 'inferno'
    bin_option: MatrixBinOption = MatrixBinOption.CONTINUOUS
    slider: List[float] = [0.0, 1.0]


class MatrixParametersStore(dcc.Store):
    """
    This class is used to represent the store for the matrix parameters.
    """
    ID = 'matrix-parameters-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=MatrixParameters().model_dump(mode='json')
        )
