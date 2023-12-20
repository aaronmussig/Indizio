import logging

from dash import Output, Input, html, callback
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.store.upload_form_store import UploadFormStore, UploadFormStoreData


class UploadFormFileSelectorContainer(html.Div):
    """
    This component wraps each of the files that are prepared for upload.
    """

    ID = 'upload-form-file-selector-container'

    def __init__(self):
        super().__init__(
            id=self.ID,
            children=list(),
            className='d-flex flex-wrap'
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
            children = list()
            for file_data in state:
                file_obj = UploadFormStoreData(**file_data)
                children.append(UploadFormFileSelector(file_obj.file_name))

            return dict(
                children=children
            )
