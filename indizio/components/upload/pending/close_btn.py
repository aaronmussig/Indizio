from typing import List, Optional

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.store.upload_form_store import UploadFormStore, UploadFormData


class UploadFormCloseButton(dbc.Button):
    """
    This is the card that is used to display each file that the user has
    uploaded. A drop-down menu option allows the user to select the
    file type.
    """
    ID = 'uploaded-form-close-button'

    def __init__(
            self,
            file_hash: str,

    ):
        super().__init__(
            id={
                'type': self.ID,
                'hash': file_hash,
            },
            className='fas fa-close px-2 py-1 mt-1',
            style={
                'marginLeft': '10px'
            }
        )


@callback(
    output=dict(
        upload_store=Output(UploadFormStore.ID, 'data', allow_duplicate=True),
    ),
    inputs=dict(
        n_clicks=Input({'type': UploadFormCloseButton.ID, 'hash': ALL}, 'n_clicks'),
        upload_store=State(UploadFormStore.ID, 'data'),
    ),
    prevent_initial_call=True
)
def close_button(n_clicks: List[Optional[int]], upload_store):
    if not n_clicks or not any(n_clicks):
        raise PreventUpdate

    # De-serialize the upload store state
    store = UploadFormData(**upload_store)

    # Extract the hash from the input
    file_hash = ctx.triggered_id['hash']

    # Remove the file from the store
    store.remove_item(file_hash)

    return dict(
        upload_store=store.model_dump(mode='json'),
    )
