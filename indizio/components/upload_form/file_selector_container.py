import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.store.upload_form_store import UploadFormStore, UploadFormData


class UploadFormFileSelectorContainer(dbc.Card):
    """
    This component wraps each of the files that are prepared for upload.
    """

    ID = 'upload-form-file-selector-container'

    def __init__(self):
        super().__init__(
            children=[
                dbc.CardHeader(
                    className='text-center',
                    children=[
                        html.B("Uploaded Files")
                    ]
                ),
                dbc.CardBody(
                    id=self.ID,
                    children=list()
                )
            ],
        )

        @callback(
            output=dict(
                children=Output(self.ID, 'children'),
            ),
            inputs=dict(
                ts=Input(UploadFormStore.ID, "modified_timestamp"),
                state=Input(UploadFormStore.ID, "data"),
            ),
        )
        def refresh_uploaded(ts, state):
            # Output debugging information
            log = logging.getLogger()

            # Check if an update should happen
            if ts is None or state is None:
                log.debug(f'{self.ID} - No action to take.')
                raise PreventUpdate

            log.debug(f'{self.ID} - Refreshing uploaded files.')
            upload_form_data = UploadFormData(**state)
            children = list()
            for file_obj in upload_form_data.data.values():
                children.append(
                    UploadFormFileSelector(
                        file_name=file_obj.file_name,
                        file_hash=file_obj.hash
                    )
                )

            return dict(
                children=children
            )
