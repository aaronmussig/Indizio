import logging

import dash_bootstrap_components as dbc
import numpy as np
from dash import Output, Input, callback
from dash import dcc, State, ctx
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE
from indizio.store.matrix_parameters import MatrixParameters


class MatrixParamsColorSlider(dbc.Row):
    ID = "matrix-params-color-slider"

    ID_BTN_MINUS = "matrix-params-color-slider-btn-minus"
    ID_BTN_PLUS = "matrix-params-color-slider-btn-plus"
    ID_RANGE = "matrix-params-color-slider-range"

    def __init__(self):
        slider_min = MatrixParameters().slider[0]
        slider_max = MatrixParameters().slider[1]
        super().__init__(
            [
                dbc.Col(
                    "Scale",
                    style={'font-weight': 'bold'},
                    width=3
                ),

                dbc.Col(
                    [
                        dbc.Button(
                            id=self.ID_BTN_MINUS,
                            className='fas fa-minus-circle ma-2'
                        ),
                        dbc.Button(
                            id=self.ID_BTN_PLUS,
                            className='fas fa-plus-circle ma-2'
                        ),
                    ],
                    width=2,
                    className='d-flex'
                ),

                dbc.Col(
                    dcc.RangeSlider(
                        id=self.ID_RANGE,
                        min=slider_min,
                        max=slider_max,
                        value=[slider_min, slider_max],
                        marks={
                            slider_min: {'label': f'{slider_min:.2f}'},
                            slider_max: {'label': f'{slider_max:.2f}'}
                        },
                        step=(slider_max - slider_max) / 100,
                        tooltip={"placement": "bottom", "always_visible": False},
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE
                    )
                )
            ]

        )

        @callback(
            output=dict(
                value=Output(self.ID_RANGE, "value"),
            ),
            inputs=dict(
                minus_clicks=Input(self.ID_BTN_MINUS, "n_clicks"),
                plus_clicks=Input(self.ID_BTN_PLUS, "n_clicks"),
                prev_value=State(self.ID_RANGE, "value"),
            ),
        )
        def toggle_slider_nodes(minus_clicks, plus_clicks, prev_value):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Adjusting matrix slider nodes.')

            if not minus_clicks and plus_clicks is None:
                log.debug(f'{self.ID} - Nothing to do.')
                raise PreventUpdate

            triggered_id = ctx.triggered_id

            print(prev_value)
            min_value = min(prev_value)
            max_value = max(prev_value)
            n_values = len(prev_value)

            # Removing a value
            if triggered_id == self.ID_BTN_MINUS:
                log.debug(f'{self.ID} - Adding node to slider.')

                if n_values <= 2:
                    log.debug(f'{self.ID} - Cannot remove more nodes.')
                    raise PreventUpdate

                return dict(
                    value=list(np.linspace(min_value, max_value, n_values - 1))
                )

            # Adding a value
            elif triggered_id == self.ID_BTN_PLUS:
                log.debug(f'{self.ID} - Removing node from slider.')
                return dict(
                    value=list(np.linspace(min_value, max_value, n_values + 1))
                )

            # Catch-all
            else:
                log.error(f'{self.ID} - Unknown trigger: {triggered_id}.')
                raise PreventUpdate
