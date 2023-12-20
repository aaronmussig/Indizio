import dash_bootstrap_components as dbc

from indizio.config import PERSISTENCE_TYPE


class NetworkThreshDegreeAIO(dbc.InputGroup):
    ID = "network-thresh-degree"

    def __init__(self):
        super().__init__(
            [
                dbc.InputGroupText("Degree (depth of neighborhood)"),
                dbc.Input(
                    id=self.ID,
                    type="number",
                    min=0,
                    step=1,
                    value=0,
                    persistence=True,
                    persistence_type=PERSISTENCE_TYPE
                ),
            ]
        )
