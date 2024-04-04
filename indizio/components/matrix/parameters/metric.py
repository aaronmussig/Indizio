import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE, ID_MATRIX_PARAMS_METRIC
from indizio.store.distance_matrix import DistanceMatrixStore, DistanceMatrixData


class MatrixParamsMetric(dbc.Row):
    """
    This component contains the option to select what data to be displayed.
    """

    ID = ID_MATRIX_PARAMS_METRIC

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Metric",
                        html_for=self.ID,
                        style={'fontWeight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=[],
                        value=None,
                        className="bg-light text-dark",
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE
                    ),
                ),
            ]
        )

        @callback(
            output=dict(
                options=Output(self.ID, "options"),
                value=Output(self.ID, "value"),
            ),
            inputs=dict(
                ts=Input(DistanceMatrixStore.ID, "modified_timestamp"),
                state=State(DistanceMatrixStore.ID, "data"),
            )
        )
        def update_values_on_dm_load(ts, state):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating matrix options based on distance matrix.')

            if ts is None or state is None:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialize the state
            state = DistanceMatrixData(**state)

            # No need to de-serialize as the key values are the file names
            options = state.as_options()
            default = options[0]['value'] if options else None
            return dict(
                options=options,
                value=default
            )
