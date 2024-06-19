import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate


class ModalDistanceMatrix(html.Div):
    ID = "upload-distance-matrix-modal"
    ID_BUTTON = f'{ID}-button'
    ID_MODAL = f'{ID}-modal'

    def __init__(self):
        super().__init__(

            children=[
                dbc.Button(
                    id=self.ID_BUTTON,
                    size='sm',
                    children='distance matrix',
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
                        dbc.ModalHeader(dbc.ModalTitle("Distance Matrix")),
                        dbc.ModalBody(
                            children=[
                                html.P(
                                    "A distance matrix should be either a tab-delimited text file or a CSV file containing numerical values."),
                                html.P(
                                    "An example table has been included below, with the corresponding text format below that."),
                                dbc.Table(
                                    children=[
                                        html.Thead(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Th(""),
                                                        html.Th("pltB"),
                                                        html.Th("aslA"),
                                                        html.Th("ssaI"),
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Tbody(
                                            children=[
                                                html.Tr(
                                                    children=[
                                                        html.Td("pltB"),
                                                        html.Td("1"),
                                                        html.Td("0.2"),
                                                        html.Td("0.1"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("aslA"),
                                                        html.Td("0.2"),
                                                        html.Td("1"),
                                                        html.Td("0.9"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("ssaI"),
                                                        html.Td("0.1"),
                                                        html.Td("0.9"),
                                                        html.Td("1"),
                                                    ]
                                                ),
                                            ]
                                        )
                                    ]

                                ),
                                html.P(html.B("File content:")),
                                html.Code(
                                    children=[
                                        ",pltB,aslA,ssaI",
                                        html.Br(),
                                        "pltB,1,0.2,0.1",
                                        html.Br(),
                                        "aslA,0.2,1,0.9",
                                        html.Br(),
                                        "ssaI,0.1,0.9,1",
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
