import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, ctx
from dash.exceptions import PreventUpdate

from indizio.components.matrix.parameters import MatrixParamsMetric, MatrixParamsColorScale, MatrixParamsColorRange, \
    MatrixParamsSyncWithNetwork
from indizio.interfaces.sync_with_network import SyncWithNetwork
from indizio.store.matrix_parameters import MatrixParametersStore, MatrixParameters


class MatrixParamsUpdateButton(dbc.Button):
    """
    This component will save the changes for the matrix parameters.
    """

    ID = "matrix-params-update-button"

    def __init__(self):
        super().__init__(
            "Update Heatmap",
            id=self.ID,
            color="success",
            n_clicks=0,
        )

        @callback(
            output=dict(
                disabled=Output(self.ID, "disabled"),
            ),
            inputs=dict(
                color_scale=Input(MatrixParamsColorScale.ID, 'value'),
                metric=Input(MatrixParamsMetric.ID, "value"),
            ),
        )
        def toggle_disabled(metric, color_scale):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Toggling update heatmap button.')

            disabled = False
            if metric is None:
                disabled = True
            if color_scale is None:
                disabled = True
            return dict(
                disabled=disabled
            )

        @callback(
            output=dict(
                params=Output(MatrixParametersStore.ID, "data"),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                metric=Input(MatrixParamsMetric.ID, "value"),
                color_scale=Input(MatrixParamsColorScale.ID, 'value'),
                color_bins=Input(MatrixParamsColorRange.ID_BIN_TEXT, 'value'),
                sync_with_network=Input(MatrixParamsSyncWithNetwork.ID, 'value'),
            ),
            prevent_initial_call=True
        )
        def update_options_on_file_upload(n_clicks, metric, color_scale, color_bins, sync_with_network):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating matrix visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # Parse the color bins
            new_bins = list()
            if color_bins and ',' in color_bins:
                for num in color_bins.split(','):
                    try:
                        new_bins.append(float(num))
                    except Exception:
                        pass
            if len(new_bins) < 2:
                new_bins = [0.0, 1.0]
            slider = sorted(set(new_bins))

            return dict(
                params=MatrixParameters(
                    metric=metric,
                    color_scale=color_scale,
                    slider=slider,
                    sync_with_network=SyncWithNetwork(sync_with_network)
                ).model_dump(mode='json')
            )
