import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State

from indizio.interfaces.boolean import BooleanYesNo
from indizio.store.clustergram_parameters import ClustergramParameters, ClustergramParametersStore


class ClustergramParamsOptimalLeafOrder(dbc.Row):
    """
    This component allows the user to select if optimal leaf ordering should be used.
    """

    ID = 'clustergram-params-optimal-leaf-order'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Optimal leaf ordering",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.RadioItems(
                        id=self.ID,
                        options=BooleanYesNo.to_options(),
                        value=ClustergramParameters().optimal_leaf_order.value,
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
            state = ClustergramParameters(**state) if state else ClustergramParameters()
            return dict(
                value=state.optimal_leaf_order.value
            )
