import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, ctx
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.parameters import ClustergramParamsMetric, ClustergramParamsTree, \
    ClustergramParamsMetadata, ClustergramParamsClusterOn, ClustergramParamsOptimalLeafOrder
from indizio.interfaces.boolean import BooleanYesNo
from indizio.interfaces.cluster_on import ClusterOn
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters


class ClustergramParamsUpdateButton(dbc.Button):
    """
    This component will store the Clustergram parameters in the store.
    """

    ID = "clustergram-params-update-button"

    def __init__(self):
        super().__init__(
            "Update Heatmap",
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
            )
        )
        def update_options_on_file_upload(n_clicks, metric, tree, metadata, cluster_on, optimal_leaf_ordering):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating clustergram visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            return dict(
                params=ClustergramParameters(
                    metric=metric,
                    tree=tree,
                    metadata=metadata,
                    cluster_on=ClusterOn(cluster_on),
                    optimal_leaf_order=BooleanYesNo(optimal_leaf_ordering),
                ).model_dump(mode='json')
            )

        @callback(
            output=dict(
                disabled=Output(self.ID, "disabled"),
            ),
            inputs=dict(
                metric=Input(ClustergramParamsMetric.ID, "value"),
                tree=Input(ClustergramParamsTree.ID, 'value'),
                cluster_on=Input(ClustergramParamsClusterOn.ID, 'value'),
                optimal_leaf_ordering=Input(ClustergramParamsOptimalLeafOrder.ID, 'value'),
            )
        )
        def toggle_disabled(metric, tree, cluster_on, optimal_leaf_ordering):
            disabled = False
            if metric is None:
                disabled = True
            if tree is None:
                disabled = True
            if cluster_on is None:
                disabled = True
            if optimal_leaf_ordering is None:
                disabled = True
            return dict(
                disabled=disabled
            )
