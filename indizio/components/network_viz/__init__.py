
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

from indizio.components.network_viz.network_graph import NetworkVizGraph
from indizio.components.network_viz.progress_bar import NetworkVizProgressBar
from indizio.components.network_viz.reset_view import NetworkVizResetView


class NetworkVizContainer(dbc.Row):
    ID = 'network-viz-container'

    def __init__(self):
        super().__init__(
            [
                NetworkVizProgressBar(),
                NetworkVizResetView(),
                NetworkVizGraph()
            ]
        )

