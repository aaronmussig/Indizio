import dash
from dash import html

from indizio import config
from indizio.components.clustergram import ClustergramContainer

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Statistics')

layout = html.Div([
    ClustergramContainer()
])

