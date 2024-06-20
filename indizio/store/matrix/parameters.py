from typing import Optional, List

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.models.common.sync_with_network import SyncWithNetwork


class MatrixParametersStoreModel(BaseModel):
    """
    This class is the actual model for the data in the matrix parameters.
    """
    metric: Optional[str] = None
    color_scale: str = 'inferno'
    slider: List[float] = [0.0, 1.0]
    sync_with_network: SyncWithNetwork = SyncWithNetwork.DISABLED


class MatrixParametersStore(dcc.Store):
    """
    This class is used to represent the store for the matrix parameters.
    """
    ID = 'matrix-parameters-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=MatrixParametersStoreModel().model_dump(mode='json')
        )
