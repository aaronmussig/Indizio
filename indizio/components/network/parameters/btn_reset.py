import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash.exceptions import PreventUpdate

from indizio.models.network.parameters import NetworkParamThreshold
from indizio.store.matrix.dm_files import DistanceMatrixStore, DistanceMatrixStoreModel
from indizio.store.network.graph import DistanceMatrixGraphStore, DistanceMatrixGraphStoreModel
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel


class NetworkFormBtnReset(dbc.Button):
    """
    This component will reset the parameters of the network.
    """

    ID = "network-form-reset-button"

    def __init__(self):
        super().__init__(
            "Reset Parameters",
            id=self.ID,
            color="danger",
            className='w-100'
        )

        # When the update button is pressed, then update the network parameters
        @callback(
            output=dict(
                network_store=Output(NetworkFormStore.ID, "data", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                state_dm=State(DistanceMatrixStore.ID, 'data'),
                state_graph=State(DistanceMatrixGraphStore.ID, 'data'),
            ),
            prevent_initial_call=True
        )
        def on_submit(n_clicks, state_dm, state_graph):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Reset network parameters.')
            if n_clicks is None:
                raise PreventUpdate

            # Load the states used to compute the original values
            dm_store = DistanceMatrixStoreModel(**state_dm)
            graph_store = DistanceMatrixGraphStoreModel(**state_graph)

            graph = graph_store.read()
            graph_nodes = frozenset(graph.nodes)
            graph_max_degree = max(d for _, d in graph.degree)

            # Reset it to the original state
            network_params = NetworkFormStoreModel()
            network_thresholds = dict()
            for cur_dm in dm_store.get_files():
                if cur_dm.file_id in network_params:
                    network_thresholds[cur_dm.file_id] = network_params[cur_dm.file_id]
                else:
                    network_thresholds[cur_dm.file_id] = NetworkParamThreshold(
                        file_id=cur_dm.file_id,
                        left_value=cur_dm.min_value if len(graph_nodes) < 100 else round(cur_dm.max_value * 0.9, 2),
                        right_value=cur_dm.max_value,
                    )
            network_params.thresholds = network_thresholds
            network_params.node_of_interest = list()
            network_params.degree.min_value = 0
            network_params.degree.max_value = graph_max_degree

            # Serialize and return the data
            return dict(
                network_store=network_params.model_dump(mode='json')
            )
