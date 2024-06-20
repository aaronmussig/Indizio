import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, dcc

from indizio.models.common.sync_with_network import SyncWithNetwork
from indizio.store.matrix.parameters import MatrixParametersStoreModel, MatrixParametersStore


class MatrixParamsSyncWithNetwork(dbc.Row):
    ID = 'matrix-params-sync-with-network'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Sync with network",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=SyncWithNetwork.to_options(),
                        value=MatrixParametersStoreModel().sync_with_network.value,
                        className="bg-light text-dark",
                        clearable=False
                    ),
                ),
            ]
        )

        @callback(
            output=dict(
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts=Input(MatrixParametersStore.ID, "modified_timestamp"),
                state=State(MatrixParametersStore.ID, "data"),
            )
        )
        def reflect_values_in_state(ts, state):
            if state is None:
                return dict(
                    value=MatrixParametersStoreModel().sync_with_network.value
                )
            state = MatrixParametersStoreModel(**state)
            return dict(
                value=state.sync_with_network.value
            )
