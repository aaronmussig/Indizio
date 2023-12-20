import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, callback

from indizio.components.console.console_interval import ConsoleInterval
from indizio.components.console.console_msg import ConsoleMsg


class ConsoleContainer(html.Div):
    ID = 'console-container'
    ID_TOGGLE_BTN = f'{ID}-toggle-btn'
    ID_CANVAS = f'{ID}-canvas'

    def __init__(self):
        super().__init__(
            children=[
                dbc.Button(
                    "Console",
                    id=self.ID_TOGGLE_BTN,
                    n_clicks=0,
                ),
                dbc.Offcanvas(
                    id=self.ID_CANVAS,
                    scrollable=True,
                    title="Console Output",
                    placement="bottom",
                    backdrop=False,
                    is_open=False,
                    children=[
                        ConsoleInterval(),
                        ConsoleMsg()
                    ]
                ),
            ])

        @callback(
            Output(self.ID_CANVAS, "is_open"),
            Input(self.ID_TOGGLE_BTN, "n_clicks"),
            State(self.ID_CANVAS, "is_open"),
        )
        def toggle_console_output(n1, is_open):
            if n1:
                return not is_open
            return is_open
