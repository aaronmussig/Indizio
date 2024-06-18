import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.layout.message import LayoutMessage
from indizio.components.upload.pending.file_selector import UploadFormFileSelector
from indizio.config import RELOAD_ID
from indizio.interfaces.file_type import UserFileType
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixFile, DistanceMatrixData
from indizio.store.dm_graph import DmGraph, DistanceMatrixGraphStore
from indizio.store.matrix_parameters import MatrixParameters, MatrixParametersStore
from indizio.store.metadata_file import MetadataFile, MetadataFileStore, MetadataData
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkParamThreshold
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceFile, PresenceAbsenceData
from indizio.store.tree_file import TreeFile, TreeFileStore, TreeData
from indizio.store.upload_form_store import UploadFormStore, UploadFormData
from indizio.util.callbacks import notify_user
from indizio.util.log import log_debug, log_info, log_warn


class UploadFormBtnUpload(dbc.Button):
    """
    This component is the button that triggers the upload and processing of files.
    """

    ID = "upload-form-upload-button"
    ID_PROGRESS = f'{ID}-progress'

    def __init__(self):
        super().__init__(
            [
                "Process",
            ],
            id=self.ID,
            color="success",
            style={
                'width': '150px',
            },
            className='me-2'
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
                message=Output(LayoutMessage.ID_MESSAGE, 'children'),
                message_ex=Output(LayoutMessage.ID_EXCEPTION, 'children'),
                message_show=Output(LayoutMessage.ID_TOAST, 'is_open'),
                matrix_params=Output(MatrixParametersStore.ID, 'data', allow_duplicate=True),
                cg_params=Output(ClustergramParametersStore.ID, 'data', allow_duplicate=True),
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
            ],
            prevent_initial_call=True,
            background=False,
        )
        def upload_content(n_clicks, values, names, state_upload, state_pa, state_dm,
                           state_meta, state_tree, state_network_params):
            """
            Processess each of the uploaded files as per their file type.

            Afterwards, the store that holds this information is cleared to save
            browser memory.
            """

            # Ensure that this was triggered by a user clicking the button
            if n_clicks is None:
                log_debug(f'{self.ID} - Nothing to do, updated prevented.')
                raise PreventUpdate
            log_debug(f'{self.ID} - Processing files: {values}')

            # Load the existing state of the stores (if present)
            try:
                pa_store = PresenceAbsenceData(**state_pa) if state_pa else PresenceAbsenceData()
                dm_store = DistanceMatrixData(**state_dm) if state_dm else DistanceMatrixData()
                meta_store = MetadataData(**state_meta) if state_meta else MetadataData()
                tree_store = TreeData(**state_tree) if state_tree else TreeData()
                upload_store = UploadFormData(**state_upload)
            except Exception as e:
                return notify_user('Unable to load previous data, restart the application and close your current tab',
                                   e)

            # This extracts the content from the pattern matching state input
            # Ignores files that do not have a file type specified
            try:
                d_file_types = dict()
                for cur_state in ctx.states_list[0]:
                    cur_type_str = cur_state['value']
                    if cur_type_str:
                        d_file_types[cur_state['id']['hash']] = UserFileType(cur_type_str)
                log_debug(f'{self.ID} - Found the following files: {d_file_types}')
            except Exception as e:
                return notify_user('Unable to parse the HTML input, please report this error', e)

            # Extract the file names provided from the pattern matching input
            try:
                d_file_names = dict()
                for cur_state in ctx.states_list[1]:
                    cur_file_name = cur_state['value']
                    if cur_file_name:
                        d_file_names[cur_state['id']['hash']] = cur_state['value']
            except Exception as e:
                return notify_user('Unable to parse file names, please report this error.', e)

            # Do nothing if no file types have been provided
            if len(d_file_types) == 0:
                return notify_user('No files were provided, ensure each file has a type.')

            # Classify the files into their respective types
            for file_obj in upload_store.data.values():
                file_type = d_file_types.get(file_obj.hash)
                file_obj.name = d_file_names.get(file_obj.hash, file_obj.name)
                if file_type is UserFileType.PA:
                    try:
                        pa_store.add_item(PresenceAbsenceFile.from_upload_data(file_obj))
                    except Exception as e:
                        return notify_user('Unable to parse the Presence/Absence file, check your formatting!', e)
                elif file_type is UserFileType.DM:
                    try:
                        dm_store.add_item(DistanceMatrixFile.from_upload_data(file_obj))
                    except Exception as e:
                        return notify_user('Unable to parse the Distance Matrix file, check your formatting!', e)
                elif file_type is UserFileType.META:
                    try:
                        meta_store.add_item(MetadataFile.from_upload_data(file_obj))
                    except Exception as e:
                        return notify_user('Unable to parse the Metadata file, check your formatting!', e)
                elif file_type is UserFileType.TREE:
                    try:
                        tree_store.add_item(TreeFile.from_upload_data(file_obj))
                    except Exception as e:
                        return notify_user('Unable to parse the Tree file, check your formatting!', e)
                else:
                    log_warn(f'{self.ID} - Skipping file: {file_obj.file_name} of unknown type {file_type}')
                    continue

            # If no distance matrices were provided, then create and calculate
            # one from the presence/absence file.
            if len(dm_store.data) == 0:
                log_info(f'{self.ID} - No distance matrices provided, creating one from presence/absence file.')
                if len(pa_store.data) == 0:
                    return notify_user('A Presence/Absence matrix must be provided.')
                # Otherwise, compute one from each presence absence file
                else:
                    for pa_file in pa_store.data.values():
                        try:
                            dm_store.add_item(pa_file.as_distance_matrix())
                        except Exception as e:
                            return notify_user(f'Unable to convert {pa_file.file_name} to a Distance Matrix.', e)

            # Create the matrix parameters default values
            first_matrix = dm_store.get_files()[0]
            matrix_params = MatrixParameters(
                metric=first_matrix.file_id,
                slider=[first_matrix.min_value, first_matrix.max_value],
            )

            # Create the graph
            try:
                graph = DmGraph.from_distance_matricies(dm_store.get_files())
            except Exception as e:
                return notify_user('Unable to create Graph from Distance Matricies.', e)

            # Load the graph
            try:
                graph_nx = graph.read()
                graph_nodes = frozenset(graph_nx.nodes)
                graph_max_degree = max(d for _, d in graph_nx.degree)
            except Exception as e:
                return notify_user('Unable to read NetworkX Graph.', e)

            # Create the network parameters
            try:
                network_params = NetworkFormStoreData(**state_network_params)
                network_thresholds = dict()
                for cur_dm in dm_store.get_files():
                    if cur_dm.file_id in network_params:
                        network_thresholds[cur_dm.file_id] = network_params[cur_dm.file_id]
                    else:
                        network_thresholds[cur_dm.file_id] = NetworkParamThreshold(
                            file_id=cur_dm.file_id,
                            left_value=cur_dm.min_value if len(graph_nodes) < 100 else round(cur_dm.max_value * 0.9, 2),
                            right_value=cur_dm.max_value,
                        )
                network_params.thresholds = network_thresholds
                network_params.node_of_interest = [x for x in network_params.node_of_interest if x in graph_nodes]
                network_params.degree.min_value = 0
                network_params.degree.max_value = graph_max_degree
            except Exception as e:
                return notify_user('Unable to create Network Parameters.', e)

            # Create the clustergram parameters
            cg_params = ClustergramParameters(
                metric=first_matrix.file_name,
                tree=tree_store.get_files()[0].file_name if len(tree_store.get_files()) > 0 else None
            )

            # Now that we've calculated everything, we need to serialize the content
            # into JSON so that it can be stored in the browser
            log_debug(f'{self.ID} - Finished processing files, returning data to stores.')
            return dict(
                pa=pa_store.model_dump(mode='json'),
                dm=dm_store.model_dump(mode='json'),
                meta=meta_store.model_dump(mode='json'),
                tree=tree_store.model_dump(mode='json'),
                graph=graph.model_dump(mode='json'),
                upload_store_clear=True,
                network_params=network_params.model_dump(mode='json'),
                reload='/',
                message='',
                message_ex='',
                message_show=False,
                matrix_params=matrix_params.model_dump(mode='json'),
                cg_params=cg_params.model_dump(mode='json'),
            )
