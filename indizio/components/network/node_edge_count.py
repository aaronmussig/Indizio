import dash_bootstrap_components as dbc

from indizio.config import ID_NETWORK_VIZ_EDGE_COUNT, ID_NETWORK_VIZ_NODE_COUNT


class NetworkVizEdgeCount(dbc.Badge):
    """
    This component shows the number of nodes and edges in the network.
    """

    ID = ID_NETWORK_VIZ_EDGE_COUNT

    def __init__(self):
        super().__init__(
            id=self.ID,
            children=[],
            pill=True,
            color='info',
            style={
                'marginLeft': '15px',
                'marginRight': '15px',
            }
        )


class NetworkVizNodeCount(dbc.Badge):
    """
    This component shows the number of nodes and edges in the network.
    """

    ID = ID_NETWORK_VIZ_NODE_COUNT

    def __init__(self):
        super().__init__(
            id=self.ID,
            children=[],
            pill=True,
            color='info',
            style={'marginLeft': '15px'}
        )
