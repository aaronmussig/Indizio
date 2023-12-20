import logging

from dash import Output, Input, html, callback, State

from indizio.components.upload_form.file_uploaded import UploadFormFileUploaded
from indizio.interfaces.file_type import UserFileType
from indizio.store.distance_matrix import DistanceMatrixFileStore, DistanceMatrixFile
from indizio.store.metadata_file import MetadataFileStore, MetadataFile
from indizio.store.presence_absence import PresenceAbsenceFileStore, PresenceAbsenceFile
from indizio.store.tree_file import TreeFileStore, TreeFile


class UploadFormFileUploadedContainer(html.Div):
    """
    This component wraps each of the files that have been processed.
    """

    ID = 'upload-form-file-uploaded-container'

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
                pa_ts=Input(PresenceAbsenceFileStore.ID, "modified_timestamp"),
                dm_ts=Input(DistanceMatrixFileStore.ID, "modified_timestamp"),
                meta_ts=Input(MetadataFileStore.ID, "modified_timestamp"),
                tree_ts=Input(TreeFileStore.ID, "modified_timestamp"),
                pa_store=State(PresenceAbsenceFileStore.ID, "data"),
                dm_store=State(DistanceMatrixFileStore.ID, "data"),
                meta_store=State(MetadataFileStore.ID, "data"),
                tree_store=State(TreeFileStore.ID, "data"),
            ),
        )
        def refresh_uploaded(pa_ts, dm_ts, meta_ts, tree_ts, pa_store, dm_store, meta_store, tree_store):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Refreshing uploaded & processed files.')

            # Deserialize the data and create a html element for each type
            children = list()
            if pa_store is not None:
                pa_file = PresenceAbsenceFile.deserialize(pa_store)

                children.append(UploadFormFileUploaded(
                    file_name=pa_file.file_name,
                    description=f'Shape: {pa_file.df.shape[0]:,} x {pa_file.df.shape[1]:,}',
                    file_type=UserFileType.PA
                ))
            if dm_store is not None:
                for dm_value in dm_store.values():
                    dm_file = DistanceMatrixFile.deserialize(dm_value)
                    children.append(UploadFormFileUploaded(
                        file_name=dm_file.file_name,
                        description=f'Shape: {dm_file.df.shape[0]:,} x {dm_file.df.shape[1]:,}',
                        file_type=UserFileType.DM
                    ))
            if meta_store is not None:
                meta_file = MetadataFile.deserialize(meta_store)
                children.append(UploadFormFileUploaded(
                    file_name=meta_file.file_name,
                    description=f'Shape: {meta_file.df.shape[0]:,} x {meta_file.df.shape[1]:,}',
                    file_type=UserFileType.META
                ))
            if tree_store is not None:
                tree_file = TreeFile.deserialize(tree_store)
                children.append(UploadFormFileUploaded(
                    file_name=tree_file.file_name,
                    description=f'Leaf nodes: {len(tree_file.taxon_namespace):,}',
                    file_type=UserFileType.TREE
                ))

            return dict(
                children=children
            )
