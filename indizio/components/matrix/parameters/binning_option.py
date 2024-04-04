import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash import State
from dash.exceptions import PreventUpdate

from indizio.store.matrix_parameters import MatrixBinOption
from indizio.store.matrix_parameters import MatrixParameters
from indizio.store.matrix_parameters import MatrixParametersStore


class MatrixParamsBinningOption(dbc.Row):
    """
    This component contains the binning option used for the matrix scale.
    """

    ID = "matrix-params-binning-option"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Aggregation",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.RadioItems(
                        options=MatrixBinOption.to_options(),
                        value=MatrixParameters().bin_option.value,
                        id=self.ID,
                        inline=True,

                    )
                )
            ]
        )

        @callback(
            output=dict(
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                mat_param_ts=Input(MatrixParametersStore.ID, "modified_timestamp"),
                mat_param_store=State(MatrixParametersStore.ID, "data"),
            ),
        )
        def refresh_to_value_in_use(mat_param_ts, mat_param_store):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Adjusting binning option.')

            if not mat_param_ts or not mat_param_store:
                log.debug(f'{self.ID} - Nothing to do.')
                raise PreventUpdate

            dm_store = MatrixParameters(**mat_param_store)

            return dict(
                value=dm_store.bin_option.value
            )
