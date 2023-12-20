from dash import dcc

from indizio.config import CONSOLE_REFRESH_MS


class ConsoleInterval(dcc.Interval):
    ID = "console-interval"

    def __init__(self):
        super().__init__(
            id=self.ID,
            interval=CONSOLE_REFRESH_MS,
            n_intervals=0,
        )
