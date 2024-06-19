import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate


class ModalPresenceAbsence(html.Div):
    ID = "upload-pa-modal"
    ID_BUTTON = f'{ID}-button'
    ID_MODAL = f'{ID}-modal'

    def __init__(self):
        super().__init__(

            children=[
                dbc.Button(
                    id=self.ID_BUTTON,
                    size='sm',
                    children='presence/absence',
                    color='link',
                    style={
                        'paddingLeft': '3px',
                        'paddingRight': '0',
                    }
                ),
                dbc.Modal(
                    id=self.ID_MODAL,
                    size="lg",
                    children=[
                        dbc.ModalHeader(dbc.ModalTitle("Presence/Absence Matrix")),
                        dbc.ModalBody(
                            children=[
                                html.P(
                                    "A presence/absence matrix should be either a tab-delimited text file or a CSV file containing either the values 1 (present), or 0 (absent)."),
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
                                                        html.Td("Campylobacter jejuni"),
                                                        html.Td("1"),
                                                        html.Td("0"),
                                                        html.Td("1"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("Haemophilus influenzae"),
                                                        html.Td("1"),
                                                        html.Td("1"),
                                                        html.Td("0"),
                                                    ]
                                                ),
                                                html.Tr(
                                                    children=[
                                                        html.Td("Helicobacter pylori"),
                                                        html.Td("1"),
                                                        html.Td("0"),
                                                        html.Td("0"),
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
                                        "Campylobacter jejuni,1,0,1",
                                        html.Br(),
                                        "Haemophilus influenzae,1,1,0",
                                        html.Br(),
                                        "Helicobacter pylori,1,0,0",
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
