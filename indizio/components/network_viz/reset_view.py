import time

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash.exceptions import PreventUpdate

from indizio.components.network_viz import NetworkVizGraph


class NetworkVizResetView(dbc.Button):
    ID = "network-viz-reset-view"

    def __init__(self):
        super().__init__(
            children=[
                "Centre graph",

            ],
            id=self.ID,
            color="warning"
        )

        @callback(
            output=dict(
                layout=Output(NetworkVizGraph.ID, "layout", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                prev_layout=Input(NetworkVizGraph.ID, "layout"),
            ),
            prevent_initial_call=True
        )
        def reset_view(n_clicks, prev_layout):
            """
            Reset the view of the cytoscape graph. This works by adding a
            a new value to the layout that will cause a refresh of the graph.
            """
            new_layout = prev_layout
            new_layout['reset-view'] = time.time()
            if n_clicks is None:
                raise PreventUpdate
            return dict(
                layout=new_layout
            )
