import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html
from dash import dcc
from dash.exceptions import PreventUpdate

from indizio.config import ID_NETWORK_PARAM_EDGE_WEIGHTS, \
    ID_NETWORK_PARAM_METRIC_SELECT
from indizio.models.network.parameters import EdgeWeights
from indizio.store.network.graph import DistanceMatrixGraphStore, DistanceMatrixGraphStoreModel
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel


class NetworkParamsDisplayProperties(dbc.Card):
    """
    This component contains the display properties for the graph.
    """

    ID = 'network-params-display-properties'
    ID_EDGE_WEIGHTS = ID_NETWORK_PARAM_EDGE_WEIGHTS
    ID_SELECT = ID_NETWORK_PARAM_METRIC_SELECT

    def __init__(self):
        super().__init__(
            className='p-0',
            children=[
                dbc.CardHeader([
                    html.B("Display Properties"),
                ],
                    className='d-flex'
                ),
                dbc.CardBody(
                    dbc.Table(
                        hover=True,
                        size='sm',
                        className='mb-0',
                        children=[
                            html.Thead(html.Tr([
                                html.Th("Attribute"),
                                html.Th("Source"),
                                html.Th("Display"),
                            ])),
                            html.Tbody([
                                html.Tr([
                                    html.Td(
                                        'Edge weights'
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=self.ID_SELECT,
                                            options=list(),
                                            value=None,
                                        ),
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=self.ID_EDGE_WEIGHTS,
                                            options=EdgeWeights.to_options(),
                                            value=None,
                                        )
                                    ),
                                ]),
                            ]),
                        ],
                    )
                )
            ],
        )

        #
        # @callback(
        #     output=dict(
        #         color_meta_options=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, 'options'),
        #         color_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, 'options'),
        #         size_meta_options=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, 'options'),
        #         size_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, 'options')
        #     ),
        #     inputs=dict(
        #         ts_meta=Input(MetadataFileStore.ID, "modified_timestamp"),
        #         state_meta=State(MetadataFileStore.ID, "data"),
        #     ),
        # )
        # def update_on_store_refresh(ts_meta, state_meta):
        #     """
        #     Updates the degree filter item when the store is refreshed.
        #     """
        #     color_meta_options = list()
        #     size_meta_options = list()
        #
        #     if ts_meta is not None:
        #         meta = MetadataData(**state_meta)
        #         for file in meta.get_files():
        #             color_meta_options.append({'label': file.file_name, 'value': file.file_id})
        #             size_meta_options.append({'label': file.file_name, 'value': file.file_id})
        #
        #     return dict(
        #         color_meta_options=color_meta_options,
        #         color_meta_columns=list(),
        #         size_meta_options=size_meta_options,
        #         size_meta_columns=list(),
        #     )
        #
        # @callback(
        #     output=dict(
        #         size_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, 'options', allow_duplicate=True),
        #     ),
        #     inputs=dict(
        #         size_meta_file=Input(ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, 'value'),
        #         state_meta=State(MetadataFileStore.ID, "data"),
        #     ),
        #     prevent_initial_call=True,
        # )
        # def update_node_size_columns(size_meta_file, state_meta):
        #     out = list()
        #     if state_meta is not None and size_meta_file is not None:
        #         meta = MetadataData(**state_meta)
        #         meta_file = meta.get_file(size_meta_file)
        #         if meta_file:
        #             for column in meta_file.read().columns:
        #                 out.append({'label': column, 'value': column})
        #     return dict(
        #         size_meta_columns=out,
        #     )
        #
        # @callback(
        #     output=dict(
        #         color_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, 'options', allow_duplicate=True),
        #     ),
        #     inputs=dict(
        #         color_meta_file=Input(ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, 'value'),
        #         state_meta=State(MetadataFileStore.ID, "data"),
        #     ),
        #     prevent_initial_call=True,
        # )
        # def update_node_color_columns(color_meta_file, state_meta):
        #     out = list()
        #     if state_meta is not None and color_meta_file is not None:
        #         meta = MetadataData(**state_meta)
        #         meta_file = meta.get_file(color_meta_file)
        #         if meta_file:
        #             for column in meta_file.read().columns:
        #                 out.append({'label': column, 'value': column})
        #     return dict(
        #         color_meta_columns=out,
        #     )
        #
        @callback(
            output=dict(
                edge_weight_metric=Output(self.ID_SELECT, 'value'),
                edge_weight_value=Output(self.ID_EDGE_WEIGHTS, 'value'),
            ),
            inputs=dict(
                ts=Input(NetworkFormStore.ID, "modified_timestamp"),
                state=State(NetworkFormStore.ID, "data"),
            ),
        )
        def update_on_store_refresh(ts, state):
            """
            Refreshes the values to match what is in the store.
            """
            if ts is None or state is None:
                raise PreventUpdate

            params = NetworkFormStoreModel(**state)

            if params.edge_weights is not None:
                edge_weight_value = params.edge_weights.value.value
                edge_weight_metric = params.edge_weights.file_id
            else:
                edge_weight_value = None
                edge_weight_metric = None

            return dict(
                edge_weight_value=edge_weight_value,
                edge_weight_metric=edge_weight_metric
            )

        @callback(
            output=dict(
                edge_weight_options=Output(self.ID_SELECT, 'options'),
            ),
            inputs=dict(
                ts=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                state=State(DistanceMatrixGraphStore.ID, "data"),
            ),
        )
        def update_on_store_refresh(ts, state):
            """
            Refreshes the values to match what is in the store.
            """
            if ts is None or state is None:
                raise PreventUpdate

            state = DistanceMatrixGraphStoreModel(**state)
            edge_weight_options = list()
            for dm_file in state.matrices:
                edge_weight_options.append({
                    'label': dm_file.file_id,
                    'value': dm_file.file_id
                })
            return dict(
                edge_weight_options=edge_weight_options
            )
