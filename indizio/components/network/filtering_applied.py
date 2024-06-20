import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, State

from indizio.config import ID_NETWORK_VIZ_FILTERING_APPLIED


class NetworkVizFilteringApplied(html.Div):
    """
    This component shows the number of nodes and edges in the network.
    """

    ID = ID_NETWORK_VIZ_FILTERING_APPLIED
    ID_TOOLTIP = f"{ID}-tooltip"

    def __init__(self):
        super().__init__(
            children=[
                dbc.Badge(
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
                ),
                dbc.Tooltip(
                    "Based on the selected parameters, not all nodes and/or edges are visible.",
                    id=self.ID_TOOLTIP,
                    target=self.ID,
                )
            ]
        )

