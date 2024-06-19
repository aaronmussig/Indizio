import dash
from dash import html

from indizio import config
from indizio.components.debug.container import DebugContainer

dash.register_page(__name__, name=f'{config.PAGE_TITLE} - Debug')

layout = html.Div(
    className='pt-3',
    children=DebugContainer()
)
