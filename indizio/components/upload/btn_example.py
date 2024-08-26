import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash.exceptions import PreventUpdate

from indizio.components.layout.reload import LayoutReload
from indizio.models.clustergram.legend import LegendGroup, LegendItem
from indizio.models.common.boolean import BooleanYesNo
from indizio.models.clustergram.cluster_on import ClusterOn
from indizio.models.distance_matrix.dm_file import DistanceMatrixFile
from indizio.models.metadata.metadata_file import MetadataFile
from indizio.models.network.parameters import NetworkParamThreshold, NetworkParamDegree, NetworkParamNodeColor, \
    NetworkParamNodeSize
from indizio.models.presence_absence.pa_file import PresenceAbsenceFile
from indizio.models.tree.tree_file import TreeFile
from indizio.models.upload.upload_file import UploadFormItem
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel
from indizio.store.clustergram.parameters import ClustergramParametersStore, ClustergramParametersStoreModel
from indizio.store.matrix.dm_files import DistanceMatrixStore, DistanceMatrixStoreModel
from indizio.store.matrix.parameters import MatrixParametersStore, MatrixParametersStoreModel
from indizio.store.metadata_file import MetadataFileStore, MetadataFileStoreModel
from indizio.store.network.graph import DistanceMatrixGraphStoreModel, DistanceMatrixGraphStore
from indizio.store.network.interaction import NetworkInteractionStore, NetworkInteractionStoreModel
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceStoreModel
from indizio.store.tree_file import TreeFileStore, TreeFileStoreModel
from indizio.store.upload_form_store import UploadFormStore
from indizio.util.package import get_package_root


class UploadFormBtnExample(dbc.Button):
    """
    This component will load the example data from: ./indizio/example
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
                clustergram_params=Output(ClustergramParametersStore.ID, "data", allow_duplicate=True),
                distance_matrix_store=Output(DistanceMatrixStore.ID, "data", allow_duplicate=True),
                dm_graph_store=Output(DistanceMatrixGraphStore.ID, "data", allow_duplicate=True),
                matrix_param_store=Output(MatrixParametersStore.ID, "data", allow_duplicate=True),
                metadata_store=Output(MetadataFileStore.ID, "data", allow_duplicate=True),
                network_store=Output(NetworkFormStore.ID, "data", allow_duplicate=True),
                network_interaction=Output(NetworkInteractionStore.ID, "data", allow_duplicate=True),
                upload_store=Output(UploadFormStore.ID, "clear_data", allow_duplicate=True),
                presence_absence_store=Output(PresenceAbsenceStore.ID, "data", allow_duplicate=True),
                tree_store=Output(TreeFileStore.ID, "data", allow_duplicate=True),
                reload=Output(LayoutReload.ID, "href", allow_duplicate=True),
                clustergram_legend=Output(ClustergramLegendStore.ID, "data", allow_duplicate=True),
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
                    file_name='Presence / Absence (Example)',
                    name='Presence / Absence (Example)',
                    path=example_dir / 'pa.tsv',
                    hash='28eef894f240bbaa1ea88a64475811c8'
                )
            )
            dm_file = DistanceMatrixFile.from_upload_data(
                UploadFormItem(
                    file_name='Matrix (Example)',
                    name='Matrix (Example)',
                    path=example_dir / 'matrix.tsv',
                    hash='95272f912a12aeca182875cedc714341'
                )
            )
            tree_file = TreeFile.from_upload_data(
                UploadFormItem(
                    file_name='Tree (Example)',
                    name='Tree (Example)',
                    path=example_dir / 'tree.nwk',
                    hash='422bd885e40e8cae0f5aded841573a98'
                )
            )
            meta_file_pa = MetadataFile.from_upload_data(
                UploadFormItem(
                    file_name='PA Metadata (Example)',
                    name='PA Metadata (Example)',
                    path=example_dir / 'metadata_pa.tsv',
                    hash='549f0e1e5a6cf1f6212994ce0ad91fbc'
                )
            )
            meta_file_graph = MetadataFile.from_upload_data(
                UploadFormItem(
                    file_name='Graph Metadata (Example)',
                    name='Graph Metadata (Example)',
                    path=example_dir / 'metadata_graph.tsv',
                    hash='462381af92bb1d76167f78d3a15b505b'
                )
            )

            # Create the stores and add their files
            pa_store = PresenceAbsenceStoreModel()
            dm_store = DistanceMatrixStoreModel()
            meta_store = MetadataFileStoreModel()
            tree_store = TreeFileStoreModel()

            clustergram_params = ClustergramParametersStoreModel(
                metric=pa_file.file_id,
                tree=tree_file.file_id,
                metadata=meta_file_pa.file_id,
                cluster_on=ClusterOn.BOTH,
                optimal_leaf_order=BooleanYesNo.YES,
                metadata_cols=['Genus', 'Factor']
            )
            matrix_params = MatrixParametersStoreModel(
                metric=dm_file.file_id,
                color_scale='agsunset',
            )

            pa_store.add_item(pa_file)
            dm_store.add_item(dm_file)
            meta_store.add_item(meta_file_pa)
            meta_store.add_item(meta_file_graph)
            tree_store.add_item(tree_file)
            graph_store = DistanceMatrixGraphStoreModel.from_distance_matricies(dm_store.get_files())

            # Compute the maximum/minimum threshold values from the distance matricies
            network_store_thresholds = dict()
            for cur_dm_file in dm_store.get_files():
                network_store_thresholds[cur_dm_file.file_id] = NetworkParamThreshold(
                    file_id=dm_file.file_id,
                    left_value=cur_dm_file.min_value,
                    right_value=cur_dm_file.max_value
                )
            network_store = NetworkFormStoreModel(
                thresholds=network_store_thresholds,
                degree=NetworkParamDegree(
                    max_value=max(x[1] for x in graph_store.read().degree),
                ),
                node_color=NetworkParamNodeColor(
                    file_id=meta_file_graph.file_id,
                    column='Group'
                ),
                node_size=NetworkParamNodeSize(
                    file_id=meta_file_graph.file_id,
                    column='Importance'
                )
            )

            clustergram_legend = ClustergramLegendStoreModel()
            clustergram_legend.groups['Genus'] = LegendGroup(
                name='Genus',
                discrete_bins={
                    'Campylobacter': LegendItem(text='Campylobacter', hex_code='#8df900'),
                    'Haemophilus': LegendItem(text='Haemophilus', hex_code='#005392'),
                    'Helicobacter': LegendItem(text='Helicobacter', hex_code='#ff7d78'),
                    'Mycobacterium': LegendItem(text='Mycobacterium', hex_code='#009192'),
                    'Staphylococcus': LegendItem(text='Staphylococcus', hex_code='#FF0000'),
                    'Streptococcus': LegendItem(text='Streptococcus', hex_code='#eaeaea'),
                }
            )
            clustergram_legend.groups['Factor'] = LegendGroup(
                name='Factor',
                continuous_bins=[0.0, 150.2],
                continuous_colorscale='agsunset'
            )

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
                network_interaction=NetworkInteractionStoreModel().model_dump(mode='json'),
                reload="/",
                clustergram_legend=clustergram_legend.model_dump(mode='json'),
            )
