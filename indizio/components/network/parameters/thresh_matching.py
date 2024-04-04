import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash.exceptions import PreventUpdate

from indizio.interfaces.boolean import BooleanAllAny
from indizio.store.network_form_store import NetworkFormStoreData, NetworkFormStore


class NetworkThreshMatching(dbc.InputGroup):
    """
    This component will allow users to select if threshold matching type.
    """

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

        @callback(
            output=dict(
                value=Output(self.ID, 'value'),
            ),
            inputs=dict(
                ts=Input(NetworkFormStore.ID, "modified_timestamp"),
                state=State(NetworkFormStore.ID, "data"),
            ),
        )
        def update_on_store_refresh(ts, state):
            """
            Updates the degree filter item when the store is refreshed.
            """
            if ts is None or state is None:
                raise PreventUpdate

            params = NetworkFormStoreData(**state)
            return dict(
                value=params.thresh_matching.value,
            )
