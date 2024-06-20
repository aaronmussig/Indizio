import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, dcc

from indizio.models.clustergram.cluster_on import ClusterOn
from indizio.store.clustergram.parameters import ClustergramParametersStoreModel, ClustergramParametersStore


class ClustergramParamsClusterOn(dbc.Row):
    """
    This component allows the user to select the clustering method.
    """

    ID = 'clustergram-params-cluster-on'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Cluster",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=ClusterOn.to_options(),
                        value=ClustergramParametersStoreModel().cluster_on.value,
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
                ts=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def reflect_values_in_state(ts, state):
            if state is None:
                return dict(
                    value=ClustergramParametersStoreModel().cluster_on.value
                )
            state = ClustergramParametersStoreModel(**state)
            return dict(
                value=state.cluster_on.value
            )
