import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, ctx
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.parameters import ClustergramParamsMetric, ClustergramParamsTree, \
    ClustergramParamsMetadata
from indizio.components.matrix.parameters import MatrixParamsMetric
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters


class ClustergramParamsUpdateButton(dbc.Button):
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
                # bin_option=Input(MatrixParamsBinningOption.ID, 'value'),
                # slider=Input(MatrixParamsColorSlider.ID_RANGE, 'value'),
            )
        )
        def update_options_on_file_upload(n_clicks, metric, tree, metadata):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating clustergram visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            return dict(
                params=ClustergramParameters(
                    metric=metric,
                    tree=tree,
                    metadata=metadata
                ).model_dump(mode='json')
            )
