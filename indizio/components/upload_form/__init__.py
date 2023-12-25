from dash import html

from indizio.components.upload_form.btn_clear import UploadFormBtnClear
from indizio.components.upload_form.btn_upload import UploadFormBtnUpload
from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.components.upload_form.file_selector_container import UploadFormFileSelectorContainer
from indizio.components.upload_form.file_upload_form import UploadFormFileUploadForm
from indizio.components.uploaded_files import UploadedFileContainer


class UploadFormContainer(html.Div):

    def __init__(self):
        super().__init__(
            [
                UploadFormFileUploadForm(),
                UploadFormFileSelectorContainer(),
                UploadedFileContainer(),
                UploadFormBtnUpload(),
                UploadFormBtnClear(),
            ]

        )
