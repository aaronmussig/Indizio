import dash
import dash_bootstrap_components as dbc

from indizio import config
from indizio.components.network_viz import NetworkVizContainer

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Network')

layout = dbc.Container(
    fluid=True,
    children=[
        NetworkVizContainer(),
    ],
)
