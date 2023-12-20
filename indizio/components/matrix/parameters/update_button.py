import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, ctx
from dash.exceptions import PreventUpdate

from indizio.components.matrix.parameters import MatrixParamsMetric, MatrixParamsColorScale, MatrixParamsBinningOption, \
    MatrixParamsColorSlider
from indizio.store.matrix_parameters import MatrixParametersStore, MatrixParameters, MatrixBinOption


class MatrixParamsUpdateButton(dbc.Button):
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
                params=Output(MatrixParametersStore.ID, "data"),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                metric=Input(MatrixParamsMetric.ID, "value"),
                color_scale=Input(MatrixParamsColorScale.ID, 'value'),
                bin_option=Input(MatrixParamsBinningOption.ID, 'value'),
                slider=Input(MatrixParamsColorSlider.ID_RANGE, 'value'),
            )
        )
        def update_options_on_file_upload(n_clicks, metric, color_scale, bin_option, slider):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating matrix visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            return dict(
                params=MatrixParameters(
                    metric=metric,
                    color_scale=color_scale,
                    bin_option=MatrixBinOption(bin_option),
                    slider=slider
                ).model_dump(mode='json')
            )
