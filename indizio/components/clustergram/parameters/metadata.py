import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, dcc

from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.metadata_file import MetadataFileStore, MetadataData


class ClustergramParamsMetadata(dbc.Row):
    """
    This component allows the user to select the metadata file used for highlighting.
    """
    ID = 'clustergram-params-metadata'
    ID_COLS = f'{ID}-cols'

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
                        placeholder='Metadata file'
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID_COLS,
                        options=[],
                        value=[],
                        className="bg-light text-dark",
                        multi=True,
                        placeholder='Columns visible'
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
            if not options:
                default = None
            else:
                default = options[0]['value'] if value is None else value

            return dict(
                options=options,
                value=default
            )

        @callback(
            output=dict(
                options=Output(self.ID_COLS, "options"),
                value=Output(self.ID_COLS, "value"),
            ),
            inputs=dict(
                metadata_value=Input(self.ID, "value"),
                state_meta=State(MetadataFileStore.ID, "data"),
                ts_params=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state_params=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def update_column_values_on_change(metadata_value, state_meta, ts_params, state_params):
            if metadata_value is None or state_meta is None:
                return dict(
                    options=list(),
                    value=list()
                )

            # De-serialize the state
            state = MetadataData(**state_meta)
            meta_file = state.get_file(metadata_value)
            meta_cols = meta_file.get_cols_as_html_options()

            # Update the state to reflect the store
            if state_params is not None:
                state_params = ClustergramParameters(**state_params)
                value = state_params.metadata_cols
            else:
                value = list()

            return dict(
                options=meta_cols,
                value=value
            )
