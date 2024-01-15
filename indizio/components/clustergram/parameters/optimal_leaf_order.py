import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE
from indizio.interfaces.boolean import BooleanYesNo
from indizio.interfaces.cluster_on import ClusterOn
from indizio.store.clustergram_parameters import ClustergramParameters
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixData
from indizio.store.tree_file import TreeFileStore, TreeData


class ClustergramParamsOptimalLeafOrder(dbc.Row):
    ID = 'clustergram-params-optimal-leaf-order'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Optimal leaf ordering",
                        html_for=self.ID,
                        style={'font-weight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.RadioItems(
                        id=self.ID,
                        options=BooleanYesNo.to_options(),
                        value=ClustergramParameters().optimal_leaf_order.value,
                        className="bg-light text-dark",
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE
                    ),
                ),
            ]
        )

        # @callback(
        #     output=dict(
        #         options=Output(self.ID, "options"),
        #         value=Output(self.ID, "value"),
        #     ),
        #     inputs=dict(
        #         ts=Input(TreeFileStore.ID, "modified_timestamp"),
        #         state=State(TreeFileStore.ID, "data"),
        #     )
        # )
        # def update_values_on_dm_load(ts, state):
        #     log = logging.getLogger()
        #     log.debug(f'{self.ID} - Updating matrix options based on distance matrix.')
        #
        #     if ts is None or state is None:
        #         log.debug(f'{self.ID} - No data to update from.')
        #         raise PreventUpdate
        #
        #     # De-serialize the state
        #     state = TreeData(**state)
        #
        #     # No need to de-serialize as the key values are the file names
        #     options = state.as_options()
        #     default = options[0]['value'] if options else None
        #     return dict(
        #         options=options,
        #         value=default
        #     )
