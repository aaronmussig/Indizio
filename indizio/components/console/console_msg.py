from dash import html, callback, Output, Input

from indizio.components.console import ConsoleInterval
from indizio.logger import DASH_LOG_HANDLER


class ConsoleMsg(html.Iframe):
    ID = "console-msg"

    def __init__(self):
        super().__init__(
            id=self.ID,
            srcDoc='',
            style={
                'width': '100%',
                'height': '400px'
            }
        )

        @callback(
            Output(self.ID, 'srcDoc'),
            Input(ConsoleInterval.ID, 'n_intervals')
        )
        def update_output(n):
            lines = list()
            for ts, lvl, msg in DASH_LOG_HANDLER.queue:
                lines.append(f'{ts} - {lvl} - {msg}')
            return "<br>".join(lines)
