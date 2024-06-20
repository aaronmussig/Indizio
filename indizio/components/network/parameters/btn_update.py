import logging

import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.network.parameters.layout import NetworkFormLayout
from indizio.components.network.parameters.node_of_interest import NetworkFormNodeOfInterest
from indizio.components.network.parameters.thresh_filter_item import NetworkThreshFilterItem
from indizio.components.network.parameters.thresh_matching import NetworkThreshMatching
from indizio.config import ID_NETWORK_FORM_DEGREE_LOWER_VALUE, ID_NETWORK_FORM_DEGREE_UPPER_VALUE, \
    ID_NETWORK_FORM_EDGES_TO_SELF, ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, \
    ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, ID_NETWORK_PARAM_EDGE_WEIGHTS, \
    ID_NETWORK_PARAM_METRIC_SELECT
from indizio.models.common.boolean import BooleanAllAny, BooleanShowHide
from indizio.models.common.bound import Bound
from indizio.models.network.parameters import EdgeWeights, NetworkFormLayoutOption, NetworkParamNodeColor, \
    NetworkParamNodeSize, NetworkParamDegree, NetworkParamThreshold, NetworkParamEdgeWeights
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel


class NetworkFormBtnUpdate(dbc.Button):
    """
    This component will store all network parameters in the store.
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

                node_color_file=State(ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, 'value'),
                node_color_column=State(ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, 'value'),
                node_size_file=State(ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, 'value'),
                node_size_column=State(ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, 'value'),

                degree_lower_value=State(ID_NETWORK_FORM_DEGREE_LOWER_VALUE, 'value'),
                degree_upper_value=State(ID_NETWORK_FORM_DEGREE_UPPER_VALUE, 'value'),
                edges_to_self=State(ID_NETWORK_FORM_EDGES_TO_SELF, 'value'),

                edge_weights=State(ID_NETWORK_PARAM_EDGE_WEIGHTS, 'value'),
                edge_weights_metric=State(ID_NETWORK_PARAM_METRIC_SELECT, 'value'),

                corr_lower_bound=State({'type': NetworkThreshFilterItem.ID_LEFT_BOUND, 'file_id': ALL}, 'value'),
                corr_upper_bound=State({'type': NetworkThreshFilterItem.ID_RIGHT_BOUND, 'file_id': ALL}, 'value'),
                corr_lower_value=State({'type': NetworkThreshFilterItem.ID_LEFT_VALUE, 'file_id': ALL}, 'value'),
                corr_upper_value=State({'type': NetworkThreshFilterItem.ID_RIGHT_VALUE, 'file_id': ALL}, 'value'),
                corr_matching=State(NetworkThreshMatching.ID, 'value'),

                # state=State(NetworkFormStore.ID, "data"),

            ),
        )
        def on_submit(
                n_clicks,
                layout,
                node_of_interest,
                node_color_file,
                node_color_column,
                node_size_file,
                node_size_column,
                degree_lower_value,
                degree_upper_value,
                edges_to_self,
                edge_weights,
                edge_weights_metric,
                corr_lower_bound,
                corr_upper_bound,
                corr_lower_value,
                corr_upper_value,
                corr_matching,
        ):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating network parameters.')
            if n_clicks is None:
                raise PreventUpdate

            # Serialise the network form state data
            network_form_state = NetworkFormStoreModel()

            network_form_state.layout = NetworkFormLayoutOption(layout)

            network_form_state.node_of_interest = node_of_interest or list()

            # Create the Node metadata options (if they're set)
            if node_color_file and node_color_column:
                network_form_state.node_color = NetworkParamNodeColor(file_id=node_color_file, column=node_color_column)
            if node_size_file and node_size_column:
                network_form_state.node_size = NetworkParamNodeSize(file_id=node_size_file, column=node_size_column)

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

            network_form_state.thresh_matching = BooleanAllAny(corr_matching)
            network_form_state.degree = NetworkParamDegree(
                min_value=min(degree_lower_value or 0.0, degree_upper_value or 1.0),
                max_value=max(degree_lower_value or 0.0, degree_upper_value or 1.0),
            )
            network_form_state.show_edges_to_self = BooleanShowHide(edges_to_self)

            if edge_weights is not None and edge_weights_metric is not None:
                network_form_state.edge_weights = NetworkParamEdgeWeights(
                    file_id=edge_weights_metric,
                    value=EdgeWeights(edge_weights)
                )

            # Serialize and return the data
            return dict(
                network_store=network_form_state.model_dump(mode='json')
            )
