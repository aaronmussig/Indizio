
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto

from indizio.components.network_viz.network_graph import NetworkVizGraph


class NetworkVizContainer(dbc.Row):
    ID = 'network-viz-container'

    def __init__(self):
        super().__init__(
            [
                NetworkVizGraph()
            ]
        )

