import dash_bootstrap_components as dbc
from dash import dcc, html

from indizio.config import PERSISTENCE_TYPE
from indizio.store.network_form_store import NetworkFormLayoutOption, NetworkFormStoreData


class NetworkFormLayout(html.Div):
    """
    This component is the drop-down menu selector for the network layout.
    """
    ID = "network-form-layout"

    def __init__(self):
        super().__init__(
            [
                dbc.Label("Change network layout", html_for=self.ID),
                dcc.Dropdown(
                    id=self.ID,
                    options=NetworkFormLayoutOption.to_options(),
                    persistence=True,
                    persistence_type=PERSISTENCE_TYPE,
                    value=NetworkFormStoreData().layout.value,
                ),
            ]
        )
