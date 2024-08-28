import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import html
from dash.exceptions import PreventUpdate

from indizio.models.network.parameters import NetworkFormLayoutOption
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel


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
                        dbc.InputGroupText(html.B("Network Layout")),
                        dbc.Select(
                            id=self.ID,
                            options=NetworkFormLayoutOption.to_options(),
                            value=NetworkFormStoreModel().layout.value,
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
            params = NetworkFormStoreModel(**state)
            return dict(
                value=params.layout.value
            )
