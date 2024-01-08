import dash_bootstrap_components as dbc
from dash import html

class ClustergramContainer(dbc.Card):
    ID = 'clustergram-container'

    def __init__(self):
        super().__init__(
            className='mt-4',
            children=[
                dbc.CardHeader(html.H4('Network Statistics')),
                dbc.CardBody([
                    "content!"
                ])
            ]
        )
