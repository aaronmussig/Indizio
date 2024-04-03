import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash.exceptions import PreventUpdate

from indizio.config import RELOAD_ID
from indizio.interfaces.boolean import BooleanYesNo
from indizio.interfaces.bound import Bound
from indizio.interfaces.cluster_on import ClusterOn
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixFile, DistanceMatrixData
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.matrix_parameters import MatrixParametersStore, MatrixParameters, MatrixBinOption
from indizio.store.metadata_file import MetadataFileStore, MetadataFile, MetadataData
from indizio.store.network_form_store import NetworkFormStore, NetworkFormLayoutOption, NetworkFormStoreData, \
    NetworkParamThreshold, NetworkParamDegree
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceFile, PresenceAbsenceData
from indizio.store.tree_file import TreeFileStore, TreeFile, TreeData
from indizio.store.upload_form_store import UploadFormStore, UploadFormData, UploadFormItem
from indizio.util.package import get_package_root


class UploadFormBtnExample(dbc.Button):
    """
    This component will load the example data.
    """

    ID = "upload-form-upload-button-example"

    def __init__(self):
        super().__init__(
            style={
                'width': '150px',
            },
            children=[
                "Load Example",
            ],
            id=self.ID,
            color="info"
        )

        @callback(
            output=dict(
                network_store=Output(NetworkFormStore.ID, "data", allow_duplicate=True),
                upload_store=Output(UploadFormStore.ID, "clear_data", allow_duplicate=True),
                presence_absence_store=Output(PresenceAbsenceStore.ID, "data", allow_duplicate=True),
                distance_matrix_store=Output(DistanceMatrixStore.ID, "data", allow_duplicate=True),
                metadata_store=Output(MetadataFileStore.ID, "data", allow_duplicate=True),
                tree_store=Output(TreeFileStore.ID, "data", allow_duplicate=True),
                dm_graph_store=Output(DistanceMatrixGraphStore.ID, "data", allow_duplicate=True),
                matrix_param_store=Output(MatrixParametersStore.ID, "data", allow_duplicate=True),
                clustergram_params=Output(ClustergramParametersStore.ID, "data", allow_duplicate=True),
                reload=Output(RELOAD_ID, "href", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
            ),
            prevent_initial_call=True
        )
        def load_example(n_clicks):
            """
            Removes all uploaded files and loads the example data.
            """

            # Output debugging information
            log = logging.getLogger()
            if n_clicks is None:
                log.debug(f'{self.ID} - No click was made, updated prevented.')
                raise PreventUpdate
            log.debug(f'{self.ID} - Resetting program to default state and loading example data.')

            # Set the paths to the example data
            pkg_root = get_package_root()
            example_dir = pkg_root / 'example'

            pa_file = PresenceAbsenceFile.from_upload_data(
                UploadFormItem(
                    file_name='pa.tsv',
                    name='Presence / Absence (Example)',
                    path=example_dir / 'pa.tsv',
                    hash='28eef894f240bbaa1ea88a64475811c8'
                )
            )
            dm_file = DistanceMatrixFile.from_upload_data(
                UploadFormItem(
                    file_name='matrix.tsv',
                    name='Matrix (Example)',
                    path=example_dir / 'matrix.tsv',
                    hash='95272f912a12aeca182875cedc714341'
                )
            )
            tree_file = TreeFile.from_upload_data(
                UploadFormItem(
                    file_name='tree.nwk',
                    name='Tree (Example)',
                    path=example_dir / 'tree.nwk',
                    hash='422bd885e40e8cae0f5aded841573a98'
                )
            )
            meta_file = MetadataFile.from_upload_data(
                UploadFormItem(
                    file_name='metadata.tsv',
                    name='Metadata (Example)',
                    path=example_dir / 'metadata.tsv',
                    hash='8df2f2b92401c5b4a8b3eeb165f924d5'
                )
            )

            # Create the stores and add their files
            pa_store = PresenceAbsenceData()
            dm_store = DistanceMatrixData()
            meta_store = MetadataData()
            tree_store = TreeData()
            network_store = NetworkFormStoreData(
                thresholds={
                    dm_file.file_id: NetworkParamThreshold(
                        file_id=dm_file.file_id,
                        left_value=0,
                        right_value=100
                    )
                },
                degree=NetworkParamDegree(
                    max_value=100.0,
                )
            )
            clustergram_params = ClustergramParameters(
                metric=pa_file.file_id,
                tree=tree_file.file_id,
                metadata=meta_file.file_id,
                cluster_on=ClusterOn.BOTH,
                optimal_leaf_order=BooleanYesNo.YES
            )
            matrix_params = MatrixParameters(
                metric=dm_file.file_id,
                color_scale='agsunset',
            )

            pa_store.add_item(pa_file)
            dm_store.add_item(dm_file)
            meta_store.add_item(meta_file)
            tree_store.add_item(tree_file)
            graph_store = DmGraph.from_distance_matricies(dm_store.get_files())

            return dict(
                network_store=network_store.model_dump(mode='json'),
                upload_store=True,
                presence_absence_store=pa_store.model_dump(mode='json'),
                distance_matrix_store=dm_store.model_dump(mode='json'),
                metadata_store=meta_store.model_dump(mode='json'),
                tree_store=tree_store.model_dump(mode='json'),
                dm_graph_store=graph_store.model_dump(mode='json'),
                clustergram_params=clustergram_params.model_dump(mode='json'),
                matrix_param_store=matrix_params.model_dump(mode='json'),
                # matrix_graph_store=True,
                # upload_form=upload_form.model_dump(mode='json'),
                reload="/"
            )
