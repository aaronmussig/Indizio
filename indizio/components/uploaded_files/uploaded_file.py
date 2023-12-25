from typing import Optional

import dash_bootstrap_components as dbc
from dash import html

from indizio.interfaces.file_type import UserFileType


class UploadedFileDisplay(dbc.Card):
    ID = 'uploaded-files-uploaded-file'

    def __init__(self, file_name: str, file_type: UserFileType, description: Optional[str] = None, name: Optional[str] = None):
        children = list()
        if name:
            children.append(file_name)
            children.append(html.Br())
        children.append(file_type.value)
        if description:
            children.append(html.Br())
            children.append(description)

        super().__init__(
            className="d-flex m-1",
            style={
                'minWidth': '250px',
            },
            children=
            [
                dbc.CardHeader(html.H5(name if name else file_name)),
                dbc.CardBody(children),
            ]
        )
