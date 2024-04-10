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
                dbc.CardHeader(html.H4('Clustergram')),
                dbc.CardBody([
                    ClustergramPlot()
                ])
            ]
        )
