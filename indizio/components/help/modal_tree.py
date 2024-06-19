import dash_bootstrap_components as dbc
from dash import Output, Input, html, callback, State
from dash.exceptions import PreventUpdate


class ModalTree(html.Div):
    ID = "upload-tree-modal"
    ID_BUTTON = f'{ID}-button'
    ID_MODAL = f'{ID}-modal'

    def __init__(self):
        super().__init__(

            children=[
                dbc.Button(
                    id=self.ID_BUTTON,
                    size='sm',
                    children='tree',
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
                        dbc.ModalHeader(dbc.ModalTitle("Tree")),
                        dbc.ModalBody(
                            children=[
                                html.P(
                                    "A tree file is expected to be in Newick format, with leaf nodes representing those used in the Presence/Absence matrix."),
                                html.P(
                                    "An example tree has been included below."),
                                html.P(html.B("File content:")),
                                html.Code(
                                    children=[
                                        "('Campylobacter jejuni':0.1,('Haemophilus influenzae':0.2,'Helicobacter pylori':0.3):0.5);"
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
