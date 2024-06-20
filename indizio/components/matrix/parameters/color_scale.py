import logging

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Output, Input, callback
from dash import dcc, State
from dash.exceptions import PreventUpdate

from indizio.store.matrix.parameters import MatrixParametersStoreModel
from indizio.store.matrix.parameters import MatrixParametersStore


class MatrixParamsColorScale(dbc.Row):
    """
    This component contains the color scale used for the matrix.
    """

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
                        value=MatrixParametersStoreModel().color_scale,
                        className="bg-light text-dark",
                        clearable=False
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

            dm_store = MatrixParametersStoreModel(**mat_param_store)

            return dict(
                value=dm_store.color_scale
            )
