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
                ts=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                state=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
            )
        )
        def update_options_on_file_upload(ts, state, state_params):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating the nodes of interest selection from user file update.')

            if ts is None or state is None:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialize the graph and return the nodes
            graph = DmGraph(**state).read()
            params = NetworkFormStoreData(**state_params)

            return dict(
                options=list(graph.nodes),
                value=params.node_of_interest
            )
