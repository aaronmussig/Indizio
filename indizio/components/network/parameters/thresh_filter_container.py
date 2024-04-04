import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html
from dash.exceptions import PreventUpdate

from indizio.components.network.parameters.thresh_filter_item import NetworkThreshFilterItem
from indizio.components.network.parameters.thresh_matching import NetworkThreshMatching
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.network_form_store import NetworkFormStoreData, NetworkParamThreshold, \
    NetworkFormStore


class NetworkThreshFilterContainer(dbc.Card):
    """
    This component contains the threshold filtering for the network.
    """

    ID = "network-thresh-filter-container"
    ID_TABLE = f"{ID}-table"

    def __init__(self):
        super().__init__(
            id=self.ID,
            className='p-0',
            children=[
                dbc.CardHeader([
                    html.B("Thresholds"),
                    html.Div([
                        NetworkThreshMatching()
                    ],
                        style={'marginLeft': 'auto', 'marginRight': '0px', 'paddingLeft': '10px'},
                    )
                ],
                    className='d-flex'
                ),
                dbc.CardBody(
                    dbc.Table([
                        html.Thead(html.Tr([
                            html.Th("Metric"),
                            html.Th("Lower bound"),
                            html.Th("Minimum value"),
                            html.Th("Maximum value"),
                            html.Th("Upper bound"),
                        ])),
                        html.Tbody(id=self.ID_TABLE),
                    ],
                        hover=True,
                        size='sm',
                        className='mb-0'
                    )
                )
            ],
        )

        @callback(
            output=dict(
                children=Output(self.ID_TABLE, 'children'),
            ),
            inputs=dict(
                ts_graph=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                ts_params=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
            ),
        )
        def update_metric(ts_graph, ts_params, state_graph, state_params):
            """
            Creates the threshold filtering options based on the items present
            in the graph. Restores any values stored in the network parameters.
            """
            if ts_graph is None or state_graph is None:
                raise PreventUpdate

            # De-serialize the state
            state = DmGraph(**state_graph)
            params = NetworkFormStoreData(**state_params)

            out = dict()
            for dm in state.matrices:
                if dm.file_id in params.thresholds:
                    out[dm.file_id] = NetworkThreshFilterItem(
                        threshold=params.thresholds[dm.file_id]
                    )
                else:
                    out[dm.file_id] = NetworkThreshFilterItem(
                        threshold=NetworkParamThreshold(
                            file_id=dm.file_id,
                            left_value=dm.min_value,
                            right_value=dm.max_value
                        )
                    )
            return dict(
                children=list(out.values()),
            )
