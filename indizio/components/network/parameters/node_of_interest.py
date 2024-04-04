import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import html, dcc
from dash.exceptions import PreventUpdate

from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData


class NetworkFormNodeOfInterest(dbc.Card):
    """
    Dropdown menu option in the network form, that allows users to
    select nodes of interest.
    """
    ID = "network-form-node-of-interest"

    def __init__(self):
        super().__init__(
            [
                dbc.CardHeader(html.B("Nodes of interest")),
                dbc.CardBody([
                    dcc.Dropdown(
                        id=self.ID,
                        options=[],
                        value=[],
                        className="bg-light text-dark",
                        multi=True,
                    ),
                ]),
            ]

        )

        @callback(
            output=dict(
                options=Output(self.ID, "options"),
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts_graph=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                ts_param=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_param=State(NetworkFormStore.ID, "data"),
            ),
        )
        def update_options_on_file_upload(ts_graph, ts_param, state_graph, state_param):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating the nodes of interest selection from user file update.')

            value = None
            if state_param is not None:
                params = NetworkFormStoreData(**state_param)
                value = params.node_of_interest

            if state_graph is None:
                return dict(
                    options=list(),
                    value=value
                )

            # De-serialize the graph and return the nodes
            graph = DmGraph(**state_graph).read()

            return dict(
                options=sorted(graph.nodes),
                value=value
            )
