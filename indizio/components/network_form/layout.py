import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import html

from indizio.config import PERSISTENCE_TYPE
from indizio.store.dm_graph import DistanceMatrixGraphStore
from indizio.store.network_form_store import NetworkFormLayoutOption
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData


class NetworkFormLayout(html.Div):
    """
    This component is the drop-down menu selector for the network layout.
    """
    ID = "network-form-layout"

    def __init__(self):
        super().__init__(
            [
                # dbc.Label("Change network layout", html_for=self.ID),
                # dcc.Dropdown(
                #     id=self.ID,
                #     options=NetworkFormLayoutOption.to_options(),
                #     persistence=True,
                #     persistence_type=PERSISTENCE_TYPE,
                #     value=NetworkFormStoreData().layout.value,
                # ),
                dbc.InputGroup([
                    dbc.InputGroupText(html.H5("Network layout")),
                    dbc.Select(
                        id=self.ID,
                        options=NetworkFormLayoutOption.to_options(),
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE,
                        value=NetworkFormStoreData().layout.value,
                    )
                ])
            ]
        )

        @callback(
            output=dict(
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                state=State(NetworkFormStore.ID, "data"),
            )
        )
        def update_options_on_file_upload(ts, state):
            params = NetworkFormStoreData(**state)
            return dict(
                value=params.layout.value
            )
