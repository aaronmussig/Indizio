import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, dcc

from indizio.config import ID_CLUSTERGRAM_PARAMS_METRIC
from indizio.store.clustergram.parameters import ClustergramParametersStore, ClustergramParametersStoreModel
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceStoreModel


class ClustergramParamsMetric(dbc.Row):
    """
    This component allows the user to select the P/A file used for the data.
    """

    ID = ID_CLUSTERGRAM_PARAMS_METRIC

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
                        clearable=False
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
                ts=Input(PresenceAbsenceStore.ID, "modified_timestamp"),
                state=State(PresenceAbsenceStore.ID, "data"),
                ts_param=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                state_param=State(ClustergramParametersStore.ID, "data"),
            )
        )
        def update_values_on_dm_load(ts, state, ts_param, state_param):
            if state is None:
                return dict(
                    options=list(),
                    value=None
                )

            value = None
            if state_param is not None:
                state_param = ClustergramParametersStoreModel(**state_param)
                value = state_param.metric

            # De-serialize the state
            state = PresenceAbsenceStoreModel(**state)

            # No need to de-serialize as the key values are the file names
            options = state.as_options()
            default = options[0]['value'] if value is None else value
            return dict(
                options=options,
                value=default
            )
