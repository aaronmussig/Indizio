import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate


from indizio.components.network_form.layout import NetworkFormLayout
from indizio.components.network_form.node_of_interest import NetworkFormNodeOfInterest
from indizio.components.network_form.thresh_filter_item import NetworkThreshFilterItem
from indizio.components.network_form.thresh_matching import NetworkThreshMatching
from indizio.config import ID_NETWORK_FORM_DEGREE_LOWER_VALUE, ID_NETWORK_FORM_DEGREE_UPPER_VALUE, \
    ID_NETWORK_FORM_EDGES_TO_SELF
from indizio.interfaces.boolean import BooleanAllAny, BooleanShowHide
from indizio.interfaces.bound import Bound
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkFormLayoutOption, \
    NetworkParamThreshold, NetworkParamDegree


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
            color="success",
            className='w-100'
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
                state=State(NetworkFormStore.ID, "data"),
                corr_lower_bound=State({'type': NetworkThreshFilterItem.ID_LEFT_BOUND, 'file_id': ALL}, 'value'),
                corr_upper_bound=State({'type': NetworkThreshFilterItem.ID_RIGHT_BOUND, 'file_id': ALL}, 'value'),
                corr_lower_value=State({'type': NetworkThreshFilterItem.ID_LEFT_VALUE, 'file_id': ALL}, 'value'),
                corr_upper_value=State({'type': NetworkThreshFilterItem.ID_RIGHT_VALUE, 'file_id': ALL}, 'value'),
                corr_matching=State(NetworkThreshMatching.ID, 'value'),
                degree_lower_value=State(ID_NETWORK_FORM_DEGREE_LOWER_VALUE, 'value'),
                degree_upper_value=State(ID_NETWORK_FORM_DEGREE_UPPER_VALUE, 'value'),
                edges_to_self=State(ID_NETWORK_FORM_EDGES_TO_SELF, 'value'),
            ),
        )
        def on_submit(
                n_clicks,
                layout,
                node_of_interest,
                state,
                corr_lower_bound,
                corr_upper_bound,
                corr_lower_value,
                corr_upper_value,
                corr_matching,
                degree_lower_value,
                degree_upper_value,
                edges_to_self
        ):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating network parameters.')
            if n_clicks is None:
                raise PreventUpdate

            # Serialise the network form state data
            network_form_state = NetworkFormStoreData(**state)
            network_form_state.layout = NetworkFormLayoutOption(layout)
            network_form_state.node_of_interest = node_of_interest or list()
            network_form_state.thresh_matching = BooleanAllAny(corr_matching)
            network_form_state.degree = NetworkParamDegree(
                min_value=min(degree_lower_value or 0.0, degree_upper_value or 1.0),
                max_value=max(degree_lower_value or 0.0, degree_upper_value or 1.0),
            )
            network_form_state.show_edges_to_self = BooleanShowHide(edges_to_self)

            # Extract the thresholds from the dynamically generated data
            d_lower_bound = dict()
            d_lower_vals = dict()
            d_upper_bound = dict()
            d_upper_vals = dict()
            for d_attr in ctx.args_grouping['corr_lower_bound']:
                d_lower_bound[d_attr['id']['file_id']] = Bound(d_attr['value'])
            for d_attr in ctx.args_grouping['corr_upper_bound']:
                d_upper_bound[d_attr['id']['file_id']] = Bound(d_attr['value'])
            for d_attr in ctx.args_grouping['corr_lower_value']:
                d_lower_vals[d_attr['id']['file_id']] = d_attr['value'] or 0.0
            for d_attr in ctx.args_grouping['corr_upper_value']:
                d_upper_vals[d_attr['id']['file_id']] = d_attr['value'] or 1.0
            file_ids = (set(d_lower_bound.keys()) & set(d_upper_bound.keys()) &
                        set(d_lower_vals.keys()) & set(d_upper_vals.keys()))
            for file_id in sorted(file_ids):
                network_form_state.thresholds[file_id] = NetworkParamThreshold(
                    file_id=file_id,
                    left_bound=d_lower_bound[file_id],
                    right_bound=d_upper_bound[file_id],
                    left_value=min(d_lower_vals[file_id], d_upper_vals[file_id]),
                    right_value=max(d_lower_vals[file_id], d_upper_vals[file_id])
                )

            # Serialize and return the data
            return dict(
                network_store=network_form_state.model_dump(mode='json')
            )
