import dash_bootstrap_components as dbc
from dash import html, dcc

from indizio.interfaces.file_type import UserFileType


class UploadFormFileSelector(dbc.Card):
    """
    This is the card that is used to display each file that the user has
    uploaded. A drop-down menu option allows the user to select the
    file type.
    """
    ID_TYPE = 'upload-form-file-selector-type'

    def __init__(self, file_name: str, file_type=None):
        self.FILE_NAME = file_name
        super().__init__(
            className="d-flex m-1",
            style={
                'minWidth': '250px',
            },
            children=
            [
                dbc.CardHeader(html.H5(self.FILE_NAME)),
                dbc.CardBody(
                    [
                        dcc.Dropdown(
                            id={
                                'type': self.ID_TYPE,
                                'name': self.FILE_NAME,
                            },
                            options=UserFileType.to_options(),
                            value=file_type,
                        ),
                    ]
                ),
            ]
        )
