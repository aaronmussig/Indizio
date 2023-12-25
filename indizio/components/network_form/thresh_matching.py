import dash_bootstrap_components as dbc

from indizio.interfaces.boolean import BooleanAllAny
from indizio.store.network_form_store import NetworkFormStoreData


class NetworkThreshMatching(dbc.InputGroup):
    ID = "network-thresh-matching"

    def __init__(self):
        super().__init__(
            children=[
                dbc.InputGroupText("Match"),
                dbc.Select(
                    id=self.ID,
                    options=BooleanAllAny.to_options(),
                    value=NetworkFormStoreData().thresh_matching.value,
                    size='sm',
                )
            ],
            size='sm'
        )
