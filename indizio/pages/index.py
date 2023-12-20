import dash
from dash import html

from indizio import config
from indizio.components.upload_form import UploadFormContainer

dash.register_page(__name__, path='/', name=config.PAGE_TITLE)

layout = html.Div([
    html.H1('INDEX'),
    html.Div('This is our Home page content.'),
    UploadFormContainer(),
])
