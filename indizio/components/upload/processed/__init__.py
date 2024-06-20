import logging

from dash import Output, Input, html, callback, State

from indizio.components.upload.processed.uploaded_file import UploadedFileDisplay
from indizio.models.common.file_type import UserFileType
from indizio.store.matrix.dm_files import DistanceMatrixStore, DistanceMatrixStoreModel
from indizio.store.metadata_file import MetadataFileStore, MetadataFileStoreModel
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceStoreModel
from indizio.store.tree_file import TreeFileStore, TreeFileStoreModel


class UploadedFileContainer(html.Div):
    """
    This component wraps each of the files that have been processed.
    """

    ID = 'uploaded-files-container'

    def __init__(self):
        super().__init__(
            id=self.ID,
            className='d-flex justify-content-center align-items-top ',
            children=list(),
        )

        @callback(
            output=dict(
                children=Output(self.ID, 'children'),
            ),
            inputs=dict(
                pa_ts=Input(PresenceAbsenceStore.ID, "modified_timestamp"),
                dm_ts=Input(DistanceMatrixStore.ID, "modified_timestamp"),
                meta_ts=Input(MetadataFileStore.ID, "modified_timestamp"),
                tree_ts=Input(TreeFileStore.ID, "modified_timestamp"),
                pa_store=State(PresenceAbsenceStore.ID, "data"),
                dm_store=State(DistanceMatrixStore.ID, "data"),
                meta_store=State(MetadataFileStore.ID, "data"),
                tree_store=State(TreeFileStore.ID, "data"),
            ),
        )
        def refresh_uploaded(pa_ts, dm_ts, meta_ts, tree_ts, pa_store, dm_store, meta_store, tree_store):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Refreshing uploaded & processed files.')

            # Deserialize the sores
            pa_store = PresenceAbsenceStoreModel(**pa_store) if pa_store else PresenceAbsenceStoreModel()
            dm_store = DistanceMatrixStoreModel(**dm_store) if dm_store else DistanceMatrixStoreModel()
            meta_store = MetadataFileStoreModel(**meta_store) if meta_store else MetadataFileStoreModel()
            tree_store = TreeFileStoreModel(**tree_store) if tree_store else TreeFileStoreModel()

            # Deserialize the data and create a html element for each type
            children = list()
            for pa_file in pa_store.get_files():
                children.append(UploadedFileDisplay(
                    file_name=pa_file.file_name,
                    name=pa_file.file_id,
                    file_type=UserFileType.PA,
                    n_cols=pa_file.n_cols,
                    n_rows=pa_file.n_rows,
                ))
            for dm_file in dm_store.get_files():
                children.append(UploadedFileDisplay(
                    file_name=dm_file.file_name,
                    name=dm_file.file_id,
                    file_type=UserFileType.DM,
                    n_cols=dm_file.n_cols,
                    n_rows=dm_file.n_rows,
                ))
            for meta_file in meta_store.get_files():
                children.append(UploadedFileDisplay(
                    file_name=meta_file.file_name,
                    name=meta_file.file_id,
                    file_type=UserFileType.META,
                    n_cols=meta_file.n_cols,
                    n_rows=meta_file.n_rows,
                ))
            for tree_file in tree_store.get_files():
                children.append(UploadedFileDisplay(
                    file_name=tree_file.file_name,
                    name=tree_file.file_id,
                    file_type=UserFileType.TREE,
                    n_leaves=tree_file.n_leaves
                ))

            return dict(
                children=children
            )
