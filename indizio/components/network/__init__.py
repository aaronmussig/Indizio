import dash_bootstrap_components as dbc
from dash import html

from indizio.components.network.btn_dl_graphml import DownloadGraphMlButton
from indizio.components.network.filtering_applied import NetworkVizFilteringApplied
from indizio.components.network.network_graph import NetworkVizGraph
from indizio.components.network.node_edge_count import NetworkVizEdgeCount, NetworkVizNodeCount
from indizio.components.network.parameters import NetworkFormParameters
from indizio.components.network.reset_view import NetworkVizResetView


class NetworkVizContainer(dbc.Card):
    """
    This component contains the network plot and action buttons.
    """

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
                            NetworkVizNodeCount(),
                            NetworkVizEdgeCount(),
                            NetworkVizFilteringApplied(),
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
