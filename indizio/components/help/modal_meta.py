import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate


class ModalMetadata(html.Div):
    ID = "upload-metadata-modal"
    ID_BUTTON = f'{ID}-button'
    ID_MODAL = f'{ID}-modal'

    def __init__(self):
        super().__init__(

            children=[
                dbc.Button(
                    id=self.ID_BUTTON,
                    size='sm',
                    children='metadata',
                    color='link',
                    style={
                        'paddingLeft': '3px',
                        'paddingRight': '3px',
                    }
                ),
                dbc.Modal(
                    id=self.ID_MODAL,
                    size="lg",
                    children=[
                        dbc.ModalHeader(dbc.ModalTitle("Metadata")),
                        dbc.ModalBody(
                            children=[
                                html.P(
                                    "A metadata file should be either a tab-delimited text file or a CSV file containing numerical or categorical values."),
                                html.P(
                                    "Indizio will attempt to determine if a column is numerical if it contains numbers, otherwise, it is assumed to be categorical."),
                                html.P(
                                    "The first column of the metadata should contain the identifier, each row should be a different sample. The first row is the column headers."),
                                html.P(
                                    "An example table has been included below, with the corresponding text format below that."),
                                dbc.Table(
                                    children=[
                                        html.Thead(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Th("Gene"),
                                                        html.Th("Group"),
                                                        html.Th("Importance"),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Tbody(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Td("pltB"),
                                                        html.Td("A"),
                                                        html.Td("30"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("aslA"),
                                                        html.Td("A"),
                                                        html.Td("45.2"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("ssaI"),
                                                        html.Td("B"),
                                                        html.Td("1.2"),
                                                    ]
                                                ),
                                            ]
                                        )
                                    ]

                                ),
                                html.P(html.B("File content:")),
                                html.Code(
                                    children=[
                                        "Gene,Group,Importance",
                                        html.Br(),
                                        "pltB,A,30",
                                        html.Br(),
                                        "aslA,A,45.2",
                                        html.Br(),
                                        "ssaI,B,1.2",
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )

        @callback(
            output=dict(
                is_open=Output(self.ID_MODAL, 'is_open'),
            ),
            inputs=dict(
                n_clicks=Input(self.ID_BUTTON, 'n_clicks'),
                is_open=State(self.ID_MODAL, 'is_open'),
            ),

        )
        def toggle_open(n_clicks, is_open):
            if n_clicks is None:
                raise PreventUpdate
            return dict(
                is_open=not is_open
            )
