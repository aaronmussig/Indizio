import base64
import logging

from dash import Output, Input, html, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.store.upload_form_store import UploadFormStore, UploadFormStoreData


class UploadFormFileUploadForm(html.Div):
    """
    This is the main component for selecting files for upload.
    """

    ID = "upload-form-file-upload-form"
    ID_FEEDBACK = "upload-form-feedback"

    def __init__(self):
        super().__init__(
            [
                dcc.Upload(
                    id=self.ID,
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=True
                ),
                html.Div(id=self.ID_FEEDBACK),
            ]

        )

        @callback(
            output=dict(
                data=Output(UploadFormStore.ID, 'data'),
            ),
            inputs=dict(
                list_of_contents=Input(self.ID, 'contents'),
                list_of_names=Input(self.ID, 'filename'),
                list_of_dates=State(self.ID, 'last_modified'),
                state=State(UploadFormStore.ID, 'data'),
            ),
        )
        def store_upload(list_of_contents, list_of_names, list_of_dates, state):
            """
            After a user has input a file, this will convert the base64 content
            into a byte string. This is then stored in the store to be processed
            on file upload.
            """
            log = logging.getLogger()
            log.debug(f'{self.ID} - {list_of_names}')

            # Do not update if no files are uploaded
            if list_of_contents is None:
                raise PreventUpdate

            output = [UploadFormStoreData(**x) for x in state]
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                content_type, content_string = c.split(',', 1)
                data_decoded = base64.b64decode(content_string)
                output.append(UploadFormStoreData(data=data_decoded, file_name=n))
            return dict(
                data=[x.model_dump(mode='json') for x in output]
            )
