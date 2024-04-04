from typing import Optional

import dash_bootstrap_components as dbc

from indizio.config import ID_NETWORK_VIZ_NODE_EDGE_COUNT


class NetworkVizNodeEdgeCount(dbc.Badge):
    """
    This component shows the number of nodes and edges in the network.
    """

    ID = ID_NETWORK_VIZ_NODE_EDGE_COUNT

    def __init__(self, node_count: Optional[int] = None, edge_count: Optional[int] = None):
        if node_count is None or edge_count is None:
            msg = 'No graph data to display'
        else:
            msg = f'Nodes: {node_count:,} | Edges: {edge_count:,}'
        super().__init__(
            id=self.ID,
            children=[
                msg
            ],
            pill=True,
            style={'marginLeft': '15px'}
        )
