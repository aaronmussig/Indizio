import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE
from indizio.store.distance_matrix import DistanceMatrixFileStore


class MatrixParamsMetric(dbc.Row):
    ID = "matrix-params-metric"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Metric",
                        html_for=self.ID,
                        style={'font-weight': 'bold'}
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
                ts=Input(DistanceMatrixFileStore.ID, "modified_timestamp"),
                state=State(DistanceMatrixFileStore.ID, "data"),
            )
        )
        def update_values_on_dm_load(ts, state):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating matrix options based on distance matrix.')

            if ts is None or state is None:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # No need to de-serialize as the key values are the file names
            options = [x for x in state.keys()]
            return dict(
                options=options,
                value=options[0] if options else None
            )
