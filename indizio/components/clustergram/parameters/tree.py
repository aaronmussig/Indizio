import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import dcc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.tree_file import TreeFileStore, TreeData


class ClustergramParamsTree(dbc.Row):
    """
    This component allows the user to specify the tree used for clustering.
    """

    ID = 'clustergram-params-tree'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Tree",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=[],
                        value=None,
                        className="bg-light text-dark",
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE,
                        clearable=False
                    ),
                ),
            ]
        )

        @callback(
            output=dict(
                options=Output(self.ID, "options"),
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts=Input(TreeFileStore.ID, "modified_timestamp"),
                state=State(TreeFileStore.ID, "data"),
                ts_param=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state_param=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def update_values_on_dm_load(ts, state, ts_param, state_param):

            if state is None:
                return dict(
                    options=list(),
                    value=None
                )

            value = None
            if state_param is not None:
                state_param = ClustergramParameters(**state_param)
                value = state_param.tree

            # De-serialize the state
            state = TreeData(**state)

            # No need to de-serialize as the key values are the file names
            options = state.as_options()
            default = options[0]['value'] if value is None else value
            return dict(
                options=options,
                value=default
            )
