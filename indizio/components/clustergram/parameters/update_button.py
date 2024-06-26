import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, ctx
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.parameters import ClustergramParamsMetric, ClustergramParamsTree, \
    ClustergramParamsMetadata, ClustergramParamsClusterOn, ClustergramParamsOptimalLeafOrder, \
    ClustergramParamsSyncWithNetwork
from indizio.models.common.boolean import BooleanYesNo
from indizio.models.clustergram.cluster_on import ClusterOn
from indizio.models.common.sync_with_network import SyncWithNetwork
from indizio.store.clustergram.parameters import ClustergramParametersStore, ClustergramParametersStoreModel


class ClustergramParamsUpdateButton(dbc.Button):
    """
    This component will store the Clustergram parameters in the store.
    """

    ID = "clustergram-params-update-button"

    def __init__(self):
        super().__init__(
            "Update Clustergram",
            id=self.ID,
            color="success",
            n_clicks=0,
        )

        @callback(
            output=dict(
                params=Output(ClustergramParametersStore.ID, "data"),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                metric=Input(ClustergramParamsMetric.ID, "value"),
                tree=Input(ClustergramParamsTree.ID, 'value'),
                metadata=Input(ClustergramParamsMetadata.ID, 'value'),
                cluster_on=Input(ClustergramParamsClusterOn.ID, 'value'),
                optimal_leaf_ordering=Input(ClustergramParamsOptimalLeafOrder.ID, 'value'),
                metadata_cols=Input(ClustergramParamsMetadata.ID_COLS, 'value'),
                sync_with_network=Input(ClustergramParamsSyncWithNetwork.ID, 'value')
            )
        )
        def update_options_on_file_upload(n_clicks, metric, tree, metadata, cluster_on, optimal_leaf_ordering, metadata_cols, sync_with_network):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating clustergram visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            return dict(
                params=ClustergramParametersStoreModel(
                    metric=metric,
                    tree=tree,
                    metadata=metadata,
                    cluster_on=ClusterOn(cluster_on),
                    optimal_leaf_order=BooleanYesNo(optimal_leaf_ordering),
                    metadata_cols=metadata_cols if metadata_cols else list(),
                    sync_with_network=SyncWithNetwork(sync_with_network)
                ).model_dump(mode='json')
            )

