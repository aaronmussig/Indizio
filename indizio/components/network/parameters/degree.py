import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html
from dash.exceptions import PreventUpdate

from indizio.config import ID_NETWORK_FORM_DEGREE_LOWER_VALUE, ID_NETWORK_FORM_DEGREE_UPPER_VALUE, \
    ID_NETWORK_FORM_DEGREE, ID_NETWORK_FORM_EDGES_TO_SELF
from indizio.interfaces.boolean import BooleanShowHide
from indizio.store.network_form_store import NetworkFormStoreData, NetworkFormStore


class NetworkFormDegree(dbc.Card):
    ID = ID_NETWORK_FORM_DEGREE
    ID_LOWER_VALUE = ID_NETWORK_FORM_DEGREE_LOWER_VALUE
    ID_UPPER_VALUE = ID_NETWORK_FORM_DEGREE_UPPER_VALUE
    ID_SHOW_EDGES_TO_SELF = ID_NETWORK_FORM_EDGES_TO_SELF

    def __init__(self):
        super().__init__(
            className='p-0',
            children=[
                dbc.CardHeader([
                    html.B("Degree (depth of neighborhood)"),
                ],
                    className='d-flex'
                ),
                dbc.CardBody(
                    dbc.Table(
                        children=[
                        html.Thead(html.Tr([
                            html.Th("Minimum"),
                            html.Th("Maximum"),
                            html.Th("Edges to self"),
                        ])),
                        html.Tbody([
                            html.Tr([
                                html.Td(
                                    dbc.Input(
                                        id=self.ID_LOWER_VALUE,
                                        type="number",
                                        value=0,
                                        step=1,
                                        size='sm'
                                    )
                                ),
                                html.Td(
                                    dbc.Input(
                                        id=self.ID_UPPER_VALUE,
                                        type="number",
                                        value=1,
                                        step=1,
                                        size='sm'
                                    )
                                ),
                                html.Td(
                                    dbc.Select(
                                        id=self.ID_SHOW_EDGES_TO_SELF,
                                        options=BooleanShowHide.to_options(),
                                        value=1,
                                        size='sm'
                                    )
                                ),
                            ])
                        ]),
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
                lower_value=Output(self.ID_LOWER_VALUE, 'value'),
                upper_value=Output(self.ID_UPPER_VALUE, 'value'),
                edges_to_self=Output(self.ID_SHOW_EDGES_TO_SELF, 'value')
            ),
            inputs=dict(
                ts_params=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_params=State(NetworkFormStore.ID, "data"),
            ),
        )
        def update_on_store_refresh(ts_params, state_params):
            """
            Updates the degree filter item when the store is refreshed.
            """
            if ts_params is None or state_params is None:
                raise PreventUpdate

            params = NetworkFormStoreData(**state_params)
            return dict(
                lower_value=params.degree.min_value,
                upper_value=params.degree.max_value,
                edges_to_self=params.show_edges_to_self.value
            )
