import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash.exceptions import PreventUpdate

from indizio.components.layout.reload import LayoutReload
from indizio.store.active_stores import ACTIVE_STORES


class UploadFormBtnClear(dbc.Button):
    """
    This component resets ALL STATES to empty. Future states need to be added here.
    """

    ID = "upload-form-upload-button-clear"

    def __init__(self):
        super().__init__(
            style={
                'width': '150px',
            },
            className='me-2',
            children=[
                "Reset",
            ],
            id=self.ID,
            color="danger"
        )

        @callback(
            output=dict(
                **{x.ID: Output(x.ID, "clear_data") for x in ACTIVE_STORES},
                reload=Output(LayoutReload.ID, "href", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
            ),
            prevent_initial_call=True
        )
        def reset_state(n_clicks):
            """
            Removes all uploaded files and resets the program.
            """

            # Output debugging information
            log = logging.getLogger()
            if n_clicks is None:
                log.debug(f'{self.ID} - No click was made, updated prevented.')
                raise PreventUpdate
            log.debug(f'{self.ID} - Resetting program to default state.')
            return dict(
                **{x.ID: True for x in ACTIVE_STORES},
                reload="/"
            )
