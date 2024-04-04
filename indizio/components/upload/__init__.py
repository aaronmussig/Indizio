import dash_bootstrap_components as dbc
from dash import html

from indizio.components.upload.btn_clear import UploadFormBtnClear
from indizio.components.upload.btn_example import UploadFormBtnExample
from indizio.components.upload.btn_upload import UploadFormBtnUpload
from indizio.components.upload.pending.file_selector_container import UploadFormFileSelectorContainer
from indizio.components.upload.pending.file_upload_form import UploadFormFileUploadForm
from indizio.components.upload.processed import UploadedFileContainer


class UploadFormContainer(html.Div):

    def __init__(self):
        super().__init__(
            className='',
            children=
            [
                dbc.Row(
                    className='justify-content-center align-items-center',
                    children=[
                        UploadFormFileUploadForm()
                    ]
                ),
                dbc.Row(
                    className='justify-content-center align-items-center mt-3',
                    children=[
                        UploadFormBtnUpload(),
                        UploadFormBtnClear(),
                        UploadFormBtnExample()
                    ]
                ),
                dbc.Row(
                    className='justify-content-center align-items-top mt-5',
                    children=[
                        UploadedFileContainer()
                    ]
                ),
            ]
        )
