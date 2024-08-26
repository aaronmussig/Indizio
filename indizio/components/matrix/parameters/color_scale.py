import logging

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, Input, callback
from dash import dcc, State
from dash.exceptions import PreventUpdate

from indizio.components.common.plotly_color_scale import CommonColorScale
from indizio.store.matrix.parameters import MatrixParametersStore
from indizio.store.matrix.parameters import MatrixParametersStoreModel


class MatrixParamsColorScale(dbc.Row):
    """
    This component contains the color scale used for the matrix.
    """

    ID = "matrix-params-color-scale"

    # Create the colour scale
    color_scale = CommonColorScale(
        identifier=ID,
        default_color=MatrixParametersStoreModel().color_scale
    )

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
                    self.color_scale
                ),

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

            dm_store = MatrixParametersStoreModel(**mat_param_store)

            return dict(
                value=dm_store.color_scale
            )
