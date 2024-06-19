import dash
from dash import html

from indizio import config
from indizio.components.help.modal_dm import ModalDistanceMatrix
from indizio.components.help.modal_meta import ModalMetadata
from indizio.components.help.modal_pa import ModalPresenceAbsence
from indizio.components.help.modal_tree import ModalTree
from indizio.components.upload import UploadFormContainer

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
                children=[
                    html.Div(
                        className='d-flex',
                        style={
                            'alignItems': 'center',
                        },
                        children=[
                            'Upload a ',
                            ModalPresenceAbsence(),
                            ', or ',
                            ModalDistanceMatrix(),
                            ' below to get started. ',
                            'Optionally, include a ',
                            ModalTree(),
                            'or ',
                            ModalMetadata(),
                            ' file.'
                        ]
                    )

                ]
            ),
        ]),
    html.Div(
        className='mt-3',
        children=[
            UploadFormContainer(),
        ]
    )
])
