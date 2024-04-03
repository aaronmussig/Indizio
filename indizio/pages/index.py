import dash
from dash import html

from indizio import config
from indizio.components.upload_form import UploadFormContainer

dash.register_page(__name__, path='/', name=config.PAGE_TITLE)

layout = html.Div([
    html.Div(
        className='d-flex flex-column align-items-center mt-3',
        children=[
            html.Div(
                html.H1('Indizio', className='display-4')
            ),
            html.Div(
                className='lead font-weight-normal',
                children='Interactively explore connected data.'
            ),
            html.Div(
                className='lead font-weight-normal mt-3',
                style={
                    'fontSize': '16px',
                },
                children='Upload a presence/absence, or distance matrix below to get started.'
            ),
        ]),
    html.Div(
        className='mt-3',
        children=[
            UploadFormContainer(),
        ]
    )
])
