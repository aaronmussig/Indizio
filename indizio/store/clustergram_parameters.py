from typing import Optional

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE
from indizio.interfaces.boolean import BooleanYesNo
from indizio.interfaces.cluster_on import ClusterOn


class ClustergramParameters(BaseModel):
    metric: Optional[str] = None
    tree: Optional[str] = None
    metadata: Optional[str] = None
    cluster_on: ClusterOn = ClusterOn.IDS
    optimal_leaf_order: BooleanYesNo = BooleanYesNo.NO


class ClustergramParametersStore(dcc.Store):
    ID = 'clustergram-parameters-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=ClustergramParameters().model_dump(mode='json')
        )
