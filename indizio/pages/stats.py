import dash
import dash_bootstrap_components as dbc
from dash import html

from indizio import config
from indizio.components.clustergram import ClustergramContainer, ClustergramParametersCanvas

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Statistics')

layout = html.Div(
    className='pt-3',
    children=[
        dbc.Row(
            [
                dbc.Col(
                    ClustergramParametersCanvas(),
                    width=4
                ),
                dbc.Col(
                    ClustergramContainer()

                )
            ]
        )
    ])
