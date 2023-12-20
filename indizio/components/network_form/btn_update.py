import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State
from dash.exceptions import PreventUpdate

from indizio.components.network_form.layout import NetworkFormLayout
from indizio.components.network_form.node_of_interest import NetworkFormNodeOfInterest
from indizio.components.network_form.thresh_corr import NetworkThreshCorrAIO
from indizio.components.network_form.thresh_degree import NetworkThreshDegreeAIO
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkFormLayoutOption, \
    NetworkThreshCorrOption


class NetworkFormBtnUpdate(dbc.Button):
    """
    This component is the "Update Network" button.

    On submission, this will update the store with the users selected parameters.
    """
    ID = "network-form-update-button"

    def __init__(self):
        super().__init__(
            "Update Network",
            id=self.ID,
            color="success"
        )

        # When the update button is pressed, then update the network parameters
        @callback(
            output=dict(
                network_store=Output(NetworkFormStore.ID, "data")
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                layout=State(NetworkFormLayout.ID, "value"),
                node_of_interest=State(NetworkFormNodeOfInterest.ID, "value"),
                thresh_degree=State(NetworkThreshDegreeAIO.ID, "value"),
                corr_select=State(NetworkThreshCorrAIO.ID_SELECT, "value"),
                corr_input=State(NetworkThreshCorrAIO.ID_INPUT, "value"),
                state=State(NetworkFormStore.ID, "data"),
            ),
        )
        def on_submit(n_clicks, layout, node_of_interest, thresh_degree, corr_select, corr_input, state):
            log = logging.getLogger()
            dbg_msg = {
                'n_clicks': n_clicks,
                'layout': layout,
                'node_of_interest': node_of_interest,
                'thresh_degree': thresh_degree,
                'corr_select': corr_select,
                'corr_input': corr_input,
                'state': state
            }
            log.debug(f'{self.ID} - {dbg_msg}')
            if n_clicks is None:
                raise PreventUpdate

            # Serialise the network form state data
            network_form_state = NetworkFormStoreData(**state)
            network_form_state.layout = NetworkFormLayoutOption(layout)
            network_form_state.node_of_interest = node_of_interest or list()
            network_form_state.thresh_degree = thresh_degree or 0
            network_form_state.thresh_corr_select = NetworkThreshCorrOption(corr_select)
            network_form_state.corr_input = corr_input or 0
            network_form_state.is_set = True

            return dict(
                network_store=network_form_state.model_dump(mode='json')
            )
