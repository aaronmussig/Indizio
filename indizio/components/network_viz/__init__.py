import dash_bootstrap_components as dbc
from dash import html

from indizio.components.network_form import NetworkFormParameters
from indizio.components.network_form.btn_dl_graphml import DownloadGraphMlButton
from indizio.components.network_viz.network_graph import NetworkVizGraph
from indizio.components.network_viz.node_edge_count import NetworkVizNodeEdgeCount
from indizio.components.network_viz.progress_bar import NetworkVizProgressBar
from indizio.components.network_viz.reset_view import NetworkVizResetView


class NetworkVizContainer(dbc.Card):
    ID = 'network-viz-container'

    def __init__(self):
        super().__init__(
            [
                dbc.CardHeader([
                    html.Div(
                        className='d-flex',
                        style={'alignItems': 'center'},
                        children=[
                            html.H4("Network Visualization", className='mt-1'),
                            NetworkVizNodeEdgeCount(),
                            html.Div(
                                className='d-flex',
                                style={'marginLeft': 'auto', 'marginRight': '0px'},
                                children=[
                                    NetworkFormParameters(),
                                    NetworkVizResetView(),
                                    DownloadGraphMlButton(),
                                ]
                            ),
                        ]
                    ),

                ]),
                dbc.CardBody([
                    NetworkVizGraph()
                ],
                    className='p-0'
                )
            ],
            className='mt-4'
        )
