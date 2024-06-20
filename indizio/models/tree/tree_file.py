from pathlib import Path

import dendropy
from pydantic import BaseModel

from indizio.models.upload.upload_file import UploadFormItem
from indizio.util.files import to_pickle, from_pickle


class TreeFile(BaseModel):
    """
    This class is the actual model for the tree file.
    """
    file_name: str
    file_id: str
    path: Path
    hash: str
    n_leaves: int

    @classmethod
    def from_upload_data(cls, data: UploadFormItem):
        """
        Convert the tree into a pickle.
        """
        tree = dendropy.Tree.get_from_path(data.path.as_posix(), schema='newick', preserve_underscores=True)
        path, md5 = to_pickle(tree)
        return cls(
            file_name=data.file_name,
            file_id=data.name,
            path=path,
            hash=md5,
            n_leaves=len(tree.taxon_namespace)
        )

    def read(self) -> dendropy.Tree:
        return from_pickle(self.path)
