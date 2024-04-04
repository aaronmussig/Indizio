import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import html
from dash.exceptions import PreventUpdate

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
                dbc.InputGroup(
                    children=[
                        dbc.InputGroupText(html.B("Network layout")),
                        dbc.Select(
                            id=self.ID,
                            options=NetworkFormLayoutOption.to_options(),
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
                ts=Input(NetworkFormStore.ID, "modified_timestamp"),
                state=State(NetworkFormStore.ID, "data"),
            )
        )
        def reflect_store_parameters(ts, state):
            if ts is None or state is None:
                raise PreventUpdate
            params = NetworkFormStoreData(**state)
            return dict(
                value=params.layout.value
            )
