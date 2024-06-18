import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback
from dash import State
from dash.exceptions import PreventUpdate

from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixData
from indizio.store.matrix_parameters import MatrixParameters, MatrixParametersStore


class MatrixParamsColorRange(dbc.Row):
    """
    This component contains the color range used for the matrix.
    """

    ID = "matrix-params-color-range"
    ID_BIN_TEXT = f"{ID}-bin-text"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    "Color Bins",
                    style={'fontWeight': 'bold'},
                    width=3
                ),
                dbc.Col(
                    dbc.Input(id=self.ID_BIN_TEXT)
                ),
            ]
        )

        @callback(
            output=dict(
                text=Output(self.ID_BIN_TEXT, "value"),
            ),
            inputs=dict(
                mat_param_ts=Input(MatrixParametersStore.ID, "modified_timestamp"),
                mat_param_store=State(MatrixParametersStore.ID, "data"),
                dm_store=State(DistanceMatrixStore.ID, "data")
            ),
        )
        def update_min_max(mat_param_ts, mat_param_store, dm_store):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Adjusting matrix slider min/max.')

            if not mat_param_store:
                log.debug(f'{self.ID} - Nothing to do.')
                raise PreventUpdate

            # Read the stored matrix value
            param_store = MatrixParameters(**mat_param_store)
            if param_store.metric is None:
                raise PreventUpdate

            # Load the file to obtain the minimum / maximum value
            dm_store = DistanceMatrixData(**dm_store)
            matrix = dm_store.get_file(param_store.metric)

            # Use the slider values set from the matrix parameters, if they exist
            # otherwise, just take the minimum and maximum value
            if param_store.slider and len(param_store.slider) >= 2:
                bin_text = ', '.join(map(str, param_store.slider))
            else:
                bin_text = f'{matrix.min_value}, {matrix.max_value}'

            return dict(
                text=bin_text
            )
