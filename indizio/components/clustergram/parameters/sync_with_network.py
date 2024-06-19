import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, dcc

from indizio.interfaces.sync_with_network import SyncWithNetwork
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters


class ClustergramParamsSyncWithNetwork(dbc.Row):
    ID = 'clustergram-params-sync-with-network'

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
                        value=ClustergramParameters().sync_with_network.value,
                        className="bg-light text-dark",
                    ),
                ),
            ]
        )

        @callback(
            output=dict(
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def reflect_values_in_state(ts, state):
            if state is None:
                return dict(
                    value=ClustergramParameters().sync_with_network.value
                )
            state = ClustergramParameters(**state)
            return dict(
                value=state.sync_with_network.value
            )
