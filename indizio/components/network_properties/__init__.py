import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate

from indizio.config import CORR_METHOD
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData


class NetworkPropertiesCard(dbc.Card):
    """
    This component shows the values that are selected in the NetworkForm component.
    """
    ID = "network-properties-card"

    ID_FOCAL_NODE = f"{ID}-focal-node"
    ID_DEGREE = f"{ID}-degree"
    ID_CORR = f"{ID}-corr"
    ID_N_NODES = f"{ID}-n-nodes"
    ID_N_EDGES = f"{ID}-n-edges"

    def __init__(self):
        super().__init__(
            [
                dbc.CardHeader(
                    html.H5("Network Properties")
                ),
                dbc.CardBody(
                    [
                        dbc.Table([
                            html.Thead(html.Tr([html.Th("Property"), html.Th("Value")])),
                            html.Tbody([
                                html.Tr([html.Td("Focal node"), html.Td(id=self.ID_FOCAL_NODE)]),
                                html.Tr([html.Td("Degree"), html.Td(id=self.ID_DEGREE)]),
                                html.Tr([html.Td("TODO (abs) thresh"), html.Td(id=self.ID_CORR)]),
                                html.Tr([html.Td("Num nodes"), html.Td(id=self.ID_N_NODES)]),
                                html.Tr([html.Td("Num edges"), html.Td(id=self.ID_N_EDGES)]),
                            ])
                        ],
                            hover=True,
                            responsive=True,
                        )
                    ]
                )
            ]
        )

        # When the update button is pressed, then update the network parameters
        @callback(
            output=dict(
                focal_node=Output(self.ID_FOCAL_NODE, "children"),
                degree=Output(self.ID_DEGREE, "children"),
                corr=Output(self.ID_CORR, "children"),
            ),
            inputs=dict(
                ts=Input(NetworkFormStore.ID, "modified_timestamp"),
                state=State(NetworkFormStore.ID, "data"),
            )
        )
        def update_values(ts, state):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID} - {{ts: {ts}, state: {state}}}')

            # Check if an update should happen
            if ts is None or state is None:
                raise PreventUpdate

            network_form_state = NetworkFormStoreData(**state)

            # Obtain the values
            focal_node = network_form_state.node_of_interest or ['All']
            focal_node = ', '.join(focal_node)

            degree = network_form_state.thresh_degree or 0
            corr_operator = network_form_state.thresh_corr_select.value
            corr_value = network_form_state.corr_input
            corr = f"{CORR_METHOD}: {corr_operator} {corr_value}"

            # Return the output values
            return dict(
                focal_node=focal_node,
                degree=degree,
                corr=corr,
            )
