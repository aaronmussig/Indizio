from typing import Optional

import dash_bootstrap_components as dbc
from dash import html

from indizio.components.upload_form.close_btn import UploadFormCloseButton
from indizio.interfaces.file_type import UserFileType


class UploadFormFileSelector(dbc.Card):
    """
    This is the card that is used to display each file that the user has
    uploaded. A drop-down menu option allows the user to select the
    file type.
    """
    ID = 'upload-form-file-selector'
    ID_TYPE = f'{ID}-type'
    ID_NAME = f'{ID}-name'

    def __init__(
            self,
            file_name: str,
            file_hash: str,
            file_type: Optional[UserFileType] = None,

    ):
        # Store identifying information
        self.FILE_HASH = file_hash

        super().__init__(
            className="d-flex m-1",
            style={
                'minWidth': '250px',
            },
            children=
            [
                dbc.CardHeader(
                    className="text-center",
                    children=[
                        html.Div(
                            className='d-flex',
                            style={'paddingLeft': '10px'},
                            children=[
                                html.H5(file_name),
                                html.Div(
                                    UploadFormCloseButton(file_hash),
                                    style={'marginLeft': 'auto', 'marginRight': '0px', 'paddingLeft': '10px'},
                                )
                            ]
                        )
                    ]
                ),
                dbc.CardBody(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText("Name", style={"minWidth": "80px"}),
                                dbc.Input(
                                    id={
                                        'type': self.ID_NAME,
                                        'hash': file_hash,
                                    },
                                    value=file_name,
                                ),
                            ]
                        ),
                        dbc.InputGroup([
                            dbc.InputGroupText("Type", style={"minWidth": "80px"}),
                            dbc.Select(
                                id={
                                    'type': self.ID_TYPE,
                                    'hash': file_hash,
                                },
                                options=UserFileType.to_options(),
                                value=file_type,
                            ),
                        ], className="mt-2"),
                    ]
                ),
            ]
        )
