import dash_bootstrap_components as dbc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.matrix_parameters import MatrixBinOption, MatrixParameters
import plotly.express as px
from dash import dcc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.matrix_parameters import MatrixParameters, MatrixParametersStore
import logging
from functools import lru_cache

import numpy as np
from dash import Output, Input, callback
from dash import dcc, State, ctx
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE, ID_MATRIX_PARAMS_METRIC
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixData
from indizio.store.matrix_parameters import MatrixParameters
from indizio.util.cache import freezeargs



class MatrixParamsBinningOption(dbc.Row):
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

