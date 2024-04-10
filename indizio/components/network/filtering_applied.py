import dash_bootstrap_components as dbc
from dash import html

from indizio.config import ID_NETWORK_VIZ_FILTERING_APPLIED


class NetworkVizFilteringApplied(dbc.Badge):
    """
    This component shows the number of nodes and edges in the network.
    """

    ID = ID_NETWORK_VIZ_FILTERING_APPLIED

    def __init__(self):
        super().__init__(
            id=self.ID,
            children=[
                html.I(
                    className='fas fa-warning me-1'
                ),
                'Filtering applied'
            ],
            pill=True,
            color='danger',
            style={
                'visibility': 'hidden'
            },
        )
