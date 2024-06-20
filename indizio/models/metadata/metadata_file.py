from pathlib import Path
from typing import Optional, Dict, List

import pandas as pd
from pydantic import BaseModel

from indizio.models.upload.upload_file import UploadFormItem
from indizio.util.files import to_pickle_df, from_pickle_df, get_delimiter


class MetadataFile(BaseModel):
    """
    This class is used to represent a single metadata file that has been uploaded.
    """
    file_name: str
    file_id: Optional[str] = None
    path: Path
    hash: str
    n_cols: int
    n_rows: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Create a metadata file from the upload data.
        """
        delimiter = get_delimiter(data.path)
        df = pd.read_table(data.path, sep=delimiter, index_col=0, encoding='latin-1')
        path, md5 = to_pickle_df(df)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            n_cols=int(df.shape[1]),
            n_rows=int(df.shape[0])
        )

    def get_cols_as_html_options(self) -> List[Dict[str, str]]:
        out = list()
        df = self.read()
        for col in df.columns:
            out.append(dict(
                label=col,
                value=col
            ))
        return out

    def read(self) -> pd.DataFrame:
        return from_pickle_df(self.path)
