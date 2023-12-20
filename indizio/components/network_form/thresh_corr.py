import dash_bootstrap_components as dbc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.network_form_store import NetworkThreshCorrOption, NetworkFormStoreData


class NetworkThreshCorrAIO(dbc.InputGroup):
    ID = "network-thresh-corr"
    ID_SELECT = f"{ID}-select"
    ID_INPUT = f"{ID}-input"
    ID_CORR = f"{ID}-corr"

    def __init__(self):
        super().__init__(
            [
                dbc.InputGroupText(
                    "TODO thresh",
                    style={"minWidth": "70%"},
                    id=self.ID_CORR
                ),
                dbc.Select(
                    id=self.ID_SELECT,
                    options=NetworkThreshCorrOption.to_options(),
                    style={"maxWidth": "15%"},
                    persistence=True,
                    persistence_type=PERSISTENCE_TYPE,
                    value=NetworkFormStoreData().thresh_corr_select.value
                ),
                dbc.Input(
                    id=self.ID_INPUT,
                    type="number",
                    value=0,
                    style={"maxWidth": "15%"},
                    persistence=True,
                    persistence_type=PERSISTENCE_TYPE
                ),
            ]
        )
