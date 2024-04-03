import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html
from dash import dcc

from indizio.config import ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, \
    ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, PERSISTENCE_TYPE
from indizio.store.metadata_file import MetadataFileStore, MetadataData


class NetworkFormNodeMetadata(dbc.Card):
    ID = 'network-form-node-metadata'

    def __init__(self):
        super().__init__(
            className='p-0',
            children=[
                dbc.CardHeader([
                    html.B("Node Metadata"),
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
                                html.Th("Target"),
                                html.Th("Metadata file"),
                                html.Th("Column"),
                            ])),
                            html.Tbody([
                                html.Tr([
                                    html.Td(
                                        'Node color'
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE,
                                            options=list(),
                                            value=None,
                                            persistence=True,
                                            persistence_type=PERSISTENCE_TYPE,
                                        )
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN,
                                            options=list(),
                                            value=None,
                                            persistence=True,
                                            persistence_type=PERSISTENCE_TYPE,
                                        )
                                    ),
                                ]),
                                html.Tr([
                                    html.Td(
                                        'Node size'
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE,
                                            options=list(),
                                            value=None,
                                            persistence=True,
                                            persistence_type=PERSISTENCE_TYPE,
                                        )
                                    ),
                                    html.Td(
                                        dcc.Dropdown(
                                            id=ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN,
                                            options=list(),
                                            value=None,
                                            persistence=True,
                                            persistence_type=PERSISTENCE_TYPE,
                                        )
                                    ),
                                ])
                            ]),
                        ],
                    )
                )
            ],
        )

        @callback(
            output=dict(
                color_meta_options=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, 'options'),
                color_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, 'options'),
                size_meta_options=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, 'options'),
                size_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, 'options')
            ),
            inputs=dict(
                ts_meta=Input(MetadataFileStore.ID, "modified_timestamp"),
                state_meta=State(MetadataFileStore.ID, "data"),
            ),
        )
        def update_on_store_refresh(ts_meta, state_meta):
            """
            Updates the degree filter item when the store is refreshed.
            """
            color_meta_options = list()
            size_meta_options = list()

            if ts_meta is not None:
                meta = MetadataData(**state_meta)
                for file in meta.get_files():
                    color_meta_options.append({'label': file.file_name, 'value': file.file_id})
                    size_meta_options.append({'label': file.file_name, 'value': file.file_id})

            return dict(
                color_meta_options=color_meta_options,
                color_meta_columns=list(),
                size_meta_options=size_meta_options,
                size_meta_columns=list(),
            )

        @callback(
            output=dict(
                size_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_SIZE_COLUMN, 'options', allow_duplicate=True),
            ),
            inputs=dict(
                size_meta_file=Input(ID_NETWORK_FORM_NODE_METADATA_SIZE_FILE, 'value'),
                state_meta=State(MetadataFileStore.ID, "data"),
            ),
            prevent_initial_call=True,
        )
        def update_node_size_columns(size_meta_file, state_meta):
            out = list()
            if state_meta is not None and size_meta_file is not None:
                meta = MetadataData(**state_meta)
                meta_file = meta.get_file(size_meta_file)
                if meta_file:
                    for column in meta_file.read().columns:
                        out.append({'label': column, 'value': column})
            return dict(
                size_meta_columns=out,
            )

        @callback(
            output=dict(
                color_meta_columns=Output(ID_NETWORK_FORM_NODE_METADATA_COLOR_COLUMN, 'options', allow_duplicate=True),
            ),
            inputs=dict(
                color_meta_file=Input(ID_NETWORK_FORM_NODE_METADATA_COLOR_FILE, 'value'),
                state_meta=State(MetadataFileStore.ID, "data"),
            ),
            prevent_initial_call=True,
        )
        def update_node_color_columns(color_meta_file, state_meta):
            out = list()
            if state_meta is not None and color_meta_file is not None:
                meta = MetadataData(**state_meta)
                meta_file = meta.get_file(color_meta_file)
                if meta_file:
                    for column in meta_file.read().columns:
                        out.append({'label': column, 'value': column})
            print(out)
            return dict(
                color_meta_columns=out,
            )
