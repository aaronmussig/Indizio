import base64
import logging

from dash import Output, Input, html, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.components.upload_form import UploadFormFileSelector
from indizio.store.upload_form_store import UploadFormStore, UploadFormItem, UploadFormData
from indizio.util.files import to_file
from indizio.util.hashing import calc_md5


class UploadFormFileUploadForm(html.Div):
    """
    This is the main component for selecting files for upload.
    """

    ID = "upload-form-file-upload-form"
    ID_PENDING = f'{ID}-pending-files'

    def __init__(self):
        super().__init__(
            className='p-3',
            style={
                'width': '100%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'minHeight': '60px',
            },
            children=[
                html.Div(
                    style={
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                    },
                    children=[
                        dcc.Upload(
                            id=self.ID,
                            children=html.Div([
                                'Drag and drop or ',
                                html.B(html.A('select files'))
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'textAlign': 'center',
                            },
                            multiple=True
                        ),
                        html.Div(
                            id=self.ID_PENDING,
                            children=[

                            ]
                        )
                    ],
                ),
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
            into a byte string. This is then stored on disk to be processed
            on file upload.
            """
            log = logging.getLogger()
            log.debug(f'{self.ID} - {list_of_names}')

            # Do not update if no files are uploaded
            if list_of_contents is None:
                raise PreventUpdate

            # Seed the output with any previously uploaded files
            output = UploadFormData(**state) if state else UploadFormData()

            # Process one or many files
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
                # Decode the content into bytes
                content_type, content_string = c.split(',', 1)
                data_decoded = base64.b64decode(content_string)

                # Generate a unique path for this file and write it to disk
                md5 = calc_md5(data_decoded)
                path = to_file(data=data_decoded, name=md5)

                # Store this file in the output
                item = UploadFormItem(path=path, file_name=n, hash=md5)
                output.add_item(item)

            return dict(
                data=output.model_dump(mode='json')
            )

        @callback(
            output=dict(
                children=Output(self.ID_PENDING, 'children'),
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
