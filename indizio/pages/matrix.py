import dash
import dash_bootstrap_components as dbc
from dash import html

from indizio import config
from indizio.components.matrix import MatrixContainer, MatrixParametersCanvas

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Matrix')

layout = html.Div(
    className='pt-3',
    children=[
        dbc.Row(
            [
                dbc.Col(
                    MatrixParametersCanvas(),
                    width=4

                ),
                dbc.Col(
                    MatrixContainer()

                )
            ]
        )
    ])
