from typing import Optional

from dash import html

from indizio.config import ID_NETWORK_VIZ_NODE_EDGE_COUNT

import dash_bootstrap_components as dbc

class NetworkVizNodeEdgeCount(dbc.Badge):
    """
    The cytoscape network graph component.
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
            # style={
            #     'backgroundColor': '#eb6864',
            #     'color': '#FFFFFF'
            # }
        )
