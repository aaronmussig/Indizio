import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.upload_form.file_selector import UploadFormFileSelector
from indizio.config import RELOAD_ID
from indizio.interfaces.bound import Bound
from indizio.interfaces.file_type import UserFileType
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixFile, DistanceMatrixData
from indizio.store.dm_graph import DmGraph, DistanceMatrixGraphStore
from indizio.store.metadata_file import MetadataFile, MetadataFileStore, MetadataData
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkParamThreshold
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceFile, PresenceAbsenceData
from indizio.store.tree_file import TreeFile, TreeFileStore, TreeData
from indizio.store.upload_form_store import UploadFormStore, UploadFormData
from indizio.util.types import ProgressFn


class UploadFormBtnUpload(dbc.Button):
    """
    This component is the button that triggers the upload and processing of files.
    """

    ID = "upload-form-upload-button"
    ID_PROGRESS = f'{ID}-progress'

    def __init__(self):
        super().__init__(
            [
                "Upload & Process",
                dbc.Progress(
                    id=self.ID_PROGRESS,
                    min=0,
                    max=100
                )
            ],
            id=self.ID,
            color="success",
        )

        @callback(
            output=dict(
                pa=Output(PresenceAbsenceStore.ID, 'data'),
                dm=Output(DistanceMatrixStore.ID, 'data'),
                meta=Output(MetadataFileStore.ID, 'data'),
                tree=Output(TreeFileStore.ID, 'data'),
                graph=Output(DistanceMatrixGraphStore.ID, 'data'),
                network_params=Output(NetworkFormStore.ID, 'data', allow_duplicate=True),
                upload_store_clear=Output(UploadFormStore.ID, 'clear_data', allow_duplicate=True),
                reload=Output(RELOAD_ID, "href", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, 'n_clicks'),
                values=State({'type': UploadFormFileSelector.ID_TYPE, 'hash': ALL}, 'value'),
                names=State({'type': UploadFormFileSelector.ID_NAME, 'hash': ALL}, 'value'),
                state_upload=State(UploadFormStore.ID, 'data'),
                state_pa=State(PresenceAbsenceStore.ID, 'data'),
                state_dm=State(DistanceMatrixStore.ID, 'data'),
                state_meta=State(MetadataFileStore.ID, 'data'),
                state_tree=State(TreeFileStore.ID, 'data'),
                state_network_params=State(NetworkFormStore.ID, 'data')
            ),
            running=[
                (Output(self.ID, "disabled"), True, False),
                # (Output(self.ID_PROGRESS, "style"), {'visibility': 'visible'}, {'visibility': 'hidden'}),
            ],
            progress=[
                Output(self.ID_PROGRESS, "value")
            ],
            prevent_initial_call=True,
            background=True,
        )
        def upload_content(set_progress: ProgressFn, n_clicks, values, names, state_upload, state_pa, state_dm,
                           state_meta,
                           state_tree, state_network_params):
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

            # Load the existing state of the stores (if present)
            pa_store = PresenceAbsenceData(**state_pa) if state_pa else PresenceAbsenceData()
            dm_store = DistanceMatrixData(**state_dm) if state_dm else DistanceMatrixData()
            meta_store = MetadataData(**state_meta) if state_meta else MetadataData()
            tree_store = TreeData(**state_tree) if state_tree else TreeData()
            upload_store = UploadFormData(**state_upload)

            # This extracts the content from the pattern matching state input
            # Ignores files that do not have a file type specified
            d_file_types = dict()
            for cur_state in ctx.states_list[0]:
                cur_type_str = cur_state['value']
                if cur_type_str:
                    d_file_types[cur_state['id']['hash']] = UserFileType(cur_type_str)
            log.debug(f'{self.ID} - Found the following files: {d_file_types}')

            # Extract the file names provided from the pattern matching input
            d_file_names = dict()
            for cur_state in ctx.states_list[1]:
                cur_file_name = cur_state['value']
                if cur_file_name:
                    d_file_names[cur_state['id']['hash']] = cur_state['value']

            # Do nothing if no file types have been provided
            if len(d_file_types) == 0:
                log.debug(f'No files were provided.')
                raise PreventUpdate

            # Classify the files into their respective types
            for file_obj in upload_store.data.values():
                file_type = d_file_types.get(file_obj.hash)
                file_obj.name = d_file_names.get(file_obj.hash, file_obj.name)
                if file_type is UserFileType.PA:
                    pa_store.add_item(PresenceAbsenceFile.from_upload_data(file_obj))
                elif file_type is UserFileType.DM:
                    dm_store.add_item(DistanceMatrixFile.from_upload_data(file_obj))
                elif file_type is UserFileType.META:
                    meta_store.add_item(MetadataFile.from_upload_data(file_obj))
                elif file_type is UserFileType.TREE:
                    tree_store.add_item(TreeFile.from_upload_data(file_obj))
                else:
                    log.warning(f'{self.ID} - Skipping file: {file_obj.file_name} of unknown type {file_type}')
                    continue

            # If no distance matrices were provided, then create and calculate
            # one from the presence/absence file.
            if len(dm_store.data) == 0:
                log.info(f'{self.ID} - No distance matrices provided, creating one from presence/absence file.')
                if len(pa_store.data) == 0:
                    log.warning(f'{self.ID} - No presence/absence file provided.')
                    raise PreventUpdate
                # Otherwise, compute one from each presence absence file
                else:
                    for pa_file in pa_store.data.values():
                        dm_store.add_item(pa_file.as_distance_matrix())

            # Create the graph
            graph = DmGraph.from_distance_matricies(dm_store.get_files(), set_progress)

            # Load the graph
            graph_nx = graph.read()
            graph_nodes = frozenset(graph_nx.nodes)
            graph_max_degree = max(d for _, d in graph_nx.degree)
            set_progress(100)

            # Create the network parameters
            network_params = NetworkFormStoreData(**state_network_params)
            network_thresholds = dict()
            for cur_dm in dm_store.get_files():
                if cur_dm.file_id in network_params:
                    network_thresholds[cur_dm.file_id] = network_params[cur_dm.file_id]
                else:
                    network_thresholds[cur_dm.file_id] = NetworkParamThreshold(
                        file_id=cur_dm.file_id,
                        left_value=cur_dm.min_value if len(graph_nodes) < 100 else round(cur_dm.max_value * 0.8, 2),
                        right_value=cur_dm.max_value,
                    )
            network_params.thresholds = network_thresholds
            network_params.node_of_interest = [x for x in network_params.node_of_interest if x in graph_nodes]
            network_params.degree.min_value = 0
            network_params.degree.max_value = graph_max_degree

            # Now that we've calculated everything, we need to serialize the content
            # into JSON so that it can be stored in the browser
            log.debug(f'{self.ID} - Finished processing files, returning data to stores.')
            return dict(
                pa=pa_store.model_dump(mode='json'),
                dm=dm_store.model_dump(mode='json'),
                meta=meta_store.model_dump(mode='json'),
                tree=tree_store.model_dump(mode='json'),
                graph=graph.model_dump(mode='json'),
                upload_store_clear=True,
                network_params=network_params.model_dump(mode='json'),
                reload='/',
            )
