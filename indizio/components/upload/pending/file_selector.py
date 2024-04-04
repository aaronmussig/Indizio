from typing import Optional

import dash_bootstrap_components as dbc

from indizio.components.upload.pending.close_btn import UploadFormCloseButton
from indizio.interfaces.file_type import UserFileType


class UploadFormFileSelector(dbc.Row):
    """
    This component is used to display a file that has been uploaded but not yet processed.
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
            className="m-1 p-2",
            style={
                'backgroundColor': "#f0f0f0",
                'borderRadius': '5px',
            },
            children=
            [
                dbc.Col(
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
                    width=6,
                ),
                dbc.Col(
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
                    ]),
                    width=5,
                ),
                dbc.Col(
                    UploadFormCloseButton(file_hash),
                    width=1,
                    className='justify-content-center align-items-center',
                ),
            ]
        )
