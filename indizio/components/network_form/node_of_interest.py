import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import html, dcc
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph


class NetworkFormNodeOfInterest(html.Div):
    """
    Dropdown menu option in the network form, that allows users to
    select nodes of interest.
    """
    ID = "network-form-node-of-interest"

    def __init__(self):
        super().__init__(
            [
                dbc.Label(
                    "Select a node of interest",
                    html_for=self.ID
                ),
                dcc.Dropdown(
                    id=self.ID,
                    options=[],
                    value=[],
                    className="bg-light text-dark",
                    multi=True,
                    persistence=True,
                    persistence_type=PERSISTENCE_TYPE
                ),
            ]

        )

        @callback(
            output=dict(
                options=Output(self.ID, "options"),
            ),
            inputs=dict(
                ts=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                state=State(DistanceMatrixGraphStore.ID, "data"),
            )
        )
        def update_options_on_file_upload(ts, state):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating the nodes of interest selection from user file update.')

            if ts is None or state is None:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialize the graph and return the nodes
            graph = DmGraph.deserialize(state)
            return dict(
                options=[x for x in graph.graph.nodes]
            )
