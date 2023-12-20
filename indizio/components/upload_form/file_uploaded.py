import logging

from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.store.upload_form_store import UploadFormStore, UploadFormStoreData
import dash_bootstrap_components as dbc
from dash import html, dcc

from indizio.interfaces.file_type import UserFileType


class UploadFormFileUploaded(dbc.Card):


    ID = 'upload-form-file-uploaded'

    def __init__(self, file_name: str, description: str, file_type: UserFileType):
        super().__init__(
            className="d-flex m-1",
            style={
                'minWidth': '250px',
            },
            children=
            [
                dbc.CardHeader(html.H5(file_name)),
                dbc.CardBody(
                    [
                        file_type.value,
                        html.Br(),
                        description,
                    ]
                ),
            ]
        )
