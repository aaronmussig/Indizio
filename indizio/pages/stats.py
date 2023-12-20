import dash
from dash import html

from indizio import config

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Statistics')

layout = html.Div([
    html.H1('STATS'),
    html.Div('This is our Home page content.'),
])

