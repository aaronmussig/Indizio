import dash_bootstrap_components as dbc
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



class MatrixParamsColorScale(dbc.Row):
    ID = "matrix-params-color-scale"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Color scale",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=px.colors.named_colorscales(),
                        value=MatrixParameters().color_scale,
                        className="bg-light text-dark",
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
            log.debug(f'{self.ID} - Adjusting matrix color scale.')

            if not mat_param_ts or not mat_param_store:
                log.debug(f'{self.ID} - Nothing to do.')
                raise PreventUpdate

            dm_store = MatrixParameters(**mat_param_store)

            return dict(
                value=dm_store.color_scale
            )

