import dash_bootstrap_components as dbc
from dash import html

from indizio.components.clustergram.clustergram_plot import ClustergramPlot
from indizio.components.clustergram.parameters import ClustergramParametersCanvas


class ClustergramContainer(dbc.Card):
    """
    This component is the main container for the clustergram plot.
    """

    ID = 'clustergram-container'

    def __init__(self):
        super().__init__(
            children=[
                dbc.CardHeader(
                    [
                        html.Div(
                            className='d-flex',
                            style={'alignItems': 'center'},
                            children=[
                                html.H4("Clustergram", className='mt-1'),
                                html.Div(
                                    className='d-flex',
                                    style={'marginLeft': 'auto', 'marginRight': '0px'},
                                    children=[
                                        ClustergramParametersCanvas(),
                                    ]
                                ),
                            ]
                        ),

                        dbc.CardBody(
                            className='p-0',
                            children=[
                                ClustergramPlot()
                            ]
                        )
                    ]
                )
            ]
        )
