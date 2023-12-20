import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.config import RELOAD_ID
from indizio.interfaces.file_type import UserFileType
from indizio.store.distance_matrix import DistanceMatrixFileStore, DistanceMatrixFile
from indizio.store.dm_graph import DmGraph, DistanceMatrixGraphStore
from indizio.store.metadata_file import MetadataFile, MetadataFileStore
from indizio.store.presence_absence import PresenceAbsenceFileStore, PresenceAbsenceFile
from indizio.store.tree_file import TreeFile, TreeFileStore
from indizio.store.upload_form_store import UploadFormStore, UploadFormStoreData


class UploadFormBtnUpload(dbc.Button):
    """
    This component is the button that triggers the upload and processing of files.
    """

    ID = "upload-form-upload-button"

    def __init__(self):
        super().__init__(
            "Upload Files",
            id=self.ID,
            color="success",
            disabled=False
        )

        @callback(
            output=dict(
                pa=Output(PresenceAbsenceFileStore.ID, 'data'),
                dm=Output(DistanceMatrixFileStore.ID, 'data'),
                meta=Output(MetadataFileStore.ID, 'data'),
                tree=Output(TreeFileStore.ID, 'data'),
                graph=Output(DistanceMatrixGraphStore.ID, 'data'),
                upload_store_clear=Output(UploadFormStore.ID, 'clear_data', allow_duplicate=True),
                reload=Output(RELOAD_ID, "href", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, 'n_clicks'),
                values=State({'type': UploadFormFileSelector.ID_TYPE, 'name': ALL}, 'value'),
                state_upload=State(UploadFormStore.ID, 'data'),
            ),
            prevent_initial_call=True,
        )
        def upload_content(n_clicks, values, state_upload):
            """
            Processess each of the uploaded files as per their file type.

            Afterwards, the store that holds this information is cleared to save
            browser memory.
            """

            # Validate the input to see if data needs to be processed.
            log = logging.getLogger()
            if n_clicks is None or not values:
                log.debug(f'{self.ID} - Nothing to do, updated prevented.')
                raise PreventUpdate
            log.debug(f'{self.ID} - Processing files: {values}')

            # This extracts the content from the pattern matching state input
            d_file_types = dict()
            for cur_state in ctx.states_list[0]:
                cur_type_str = cur_state['value']
                if cur_type_str is None:
                    d_file_types[cur_state['id']['name']] = None
                else:
                    d_file_types[cur_state['id']['name']] = UserFileType(cur_type_str)
            log.debug(f'{self.ID} - Found the following files: {d_file_types}')

            # Convert each of the uploaded files into objects
            lst_files_pa = list()
            lst_files_dm = list()
            lst_files_meta = list()
            lst_files_tree = list()
            for file_json in state_upload:
                file_obj = UploadFormStoreData(**file_json)
                file_type = d_file_types[file_obj.file_name]
                if file_type is UserFileType.PA:
                    lst_files_pa.append(file_obj)
                elif file_type is UserFileType.DM:
                    lst_files_dm.append(file_obj)
                elif file_type is UserFileType.META:
                    lst_files_meta.append(file_obj)
                elif file_type is UserFileType.TREE:
                    lst_files_tree.append(file_obj)
                else:
                    log.warning(f'{self.ID} - Skipping file: {file_obj.file_name} of unknown type {file_type}')
                    continue

            # TODO: Validate that the correct number of input files were provided.
            if len(lst_files_pa) > 1:
                log.warning(f'{self.ID} - Only one P/A table is allowed.')
                raise PreventUpdate
            if len(lst_files_meta) > 1:
                log.warning(f'{self.ID} - Only one metadata file is allowed.')
                raise PreventUpdate
            if len(lst_files_tree) > 1:
                log.warning(f'{self.ID} - Only one tree file is allowed.')
                raise PreventUpdate

            # Now that we've validated the file are correct, insert them
            # into a dictionary for further processing
            d_files = dict()
            if len(lst_files_pa) > 0:
                d_files[lst_files_pa[0].file_name] = lst_files_pa[0]
            if len(lst_files_dm) > 0:
                for cur_file in lst_files_dm:
                    d_files[cur_file.file_name] = cur_file
            if len(lst_files_meta) > 0:
                d_files[lst_files_meta[0].file_name] = lst_files_meta[0]
            if len(lst_files_tree) > 0:
                d_files[lst_files_tree[0].file_name] = lst_files_tree[0]

            """
            Determine what needs to be done based on the files that were uploaded.
            
            1. Only one P/A table is allowed.
            2. Multiple distance matricies are allowed.
            3. Only one metadata file is allowed.
            4. Only one tree file is allowed.
            
            - If no DMs are provided, then calc Pearson corr from P/A.
            - If a P/A table exists, and a tree is provided, then subset tree to P/A values (pa.index).
            """

            # TODO: Verify that the above rules are met based on the files given
            out_pa_file = None
            out_distance_matrices = dict()
            out_meta_file = None
            out_tree_file = None

            # Process each file depending on the type
            for file_name, file_obj in d_files.items():
                file_type = d_file_types[file_name]
                log.debug(f'{self.ID} - Processing file: {file_name} of type {file_type}')

                # Presence/absence file
                if file_type is UserFileType.PA:
                    log.debug(f'{self.ID} - Processing presence/absence file: {file_name}')
                    out_pa_file = PresenceAbsenceFile.from_upload_data(file_obj)

                # Distance matrix file
                elif file_type is UserFileType.DM:
                    log.debug(f'{self.ID} - Processing distance matrix file: {file_name}')
                    out_distance_matrices[file_name] = DistanceMatrixFile.from_upload_data(file_obj)

                # Metadata file
                elif file_type is UserFileType.META:
                    log.debug(f'{self.ID} - Processing metadata file: {file_name}')
                    out_meta_file = MetadataFile.from_upload_data(file_obj)

                # Tree file
                elif file_type is UserFileType.TREE:
                    log.debug(f'{self.ID} - Processing tree file: {file_name}')
                    out_tree_file = TreeFile.from_upload_data(file_obj)

                # Unknown file type
                else:
                    log.warning(f'{self.ID} - Skipping file: {file_name} of type {file_type}')

            # If no distance matrices were provided, then create and calculate
            # one from the presence/absence file.
            if len(out_distance_matrices) == 0:
                log.info(f'{self.ID} - No distance matrices provided, creating one from presence/absence file.')
                if out_pa_file is None:
                    log.warning(f'{self.ID} - No presence/absence file provided.')
                    raise PreventUpdate
                else:
                    out_distance_matrices[out_pa_file.file_name] = out_pa_file.as_distance_matrix()

            # Create the graph
            graph = DmGraph.from_distance_matricies(list(out_distance_matrices.values()))

            # Now that we've calculated everything, we need to serialize the content
            # into JSON so that it can be stored in the browser
            out_pa_file = out_pa_file.serialize() if out_pa_file else None
            out_distance_matrices = {k: v.serialize() for k, v in out_distance_matrices.items()}
            out_meta_file = out_meta_file.serialize() if out_meta_file else None
            out_tree_file = out_tree_file.serialize() if out_tree_file else None
            out_graph = graph.serialize() if graph else None

            log.debug(f'{self.ID} - Finished processing files, returning data to stores.')
            return dict(
                pa=out_pa_file,
                dm=out_distance_matrices,
                meta=out_meta_file,
                tree=out_tree_file,
                graph=out_graph,
                upload_store_clear=True,
                reload=None,
            )
