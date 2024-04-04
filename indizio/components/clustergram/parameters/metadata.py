import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.config import PERSISTENCE_TYPE
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.metadata_file import MetadataFileStore, MetadataData


class ClustergramParamsMetadata(dbc.Row):
    ID = 'clustergram-params-metadata'

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Metadata",
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
                ts=Input(MetadataFileStore.ID, "modified_timestamp"),
                state=State(MetadataFileStore.ID, "data"),
                ts_params=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state_params=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def update_values_on_dm_load(ts, state, ts_params, state_params):
            if state is None:
                return dict(
                    options=list(),
                    value=None
                )

            value = None
            if state_params is not None:
                state_params = ClustergramParameters(**state_params)
                value = state_params.metadata

            # De-serialize the state
            state = MetadataData(**state)

            # No need to de-serialize as the key values are the file names
            options = state.as_options()
            default = options[0]['value'] if value is None else value
            return dict(
                options=options,
                value=default
            )
