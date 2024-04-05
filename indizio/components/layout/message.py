import dash_bootstrap_components as dbc
from dash import html


class LayoutMessage(dbc.Toast):
    """
    This component is generally used to provide feedback to the user.
    """

    ID = "layout-message"
    ID_TOAST = f'{ID}-toast'
    ID_MESSAGE = f'{ID}-message'
    ID_EXCEPTION = f'{ID}-exception'
    DISPLAY_SEC = 10

    def __init__(self):
        super().__init__(
            id=self.ID_TOAST,
            dismissable=True,
            is_open=False,
            duration=1000 * self.DISPLAY_SEC,
            icon="info",
            children=[
                html.Div(id=self.ID_MESSAGE),
                html.Br(),
                html.Code(
                    id=self.ID_EXCEPTION,
                )
            ],
            header=[
                "Notifications",
            ],
            style={
                "position": "fixed",
                "top": 66,
                "right": 10,
                "width": 500,
                "zIndex": 9000,
                "backgroundColor": "#FFFFFF"
            },
        ),
