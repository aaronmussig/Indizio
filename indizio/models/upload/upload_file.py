from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class UploadFormItem(BaseModel):
    """
    This class represents the data that is stored in the upload form store.
    """
    file_name: str
    name: str
    path: Path
    hash: str
