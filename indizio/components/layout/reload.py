from dash import dcc


class LayoutReload(dcc.Location):
    """
    Used to control the URL.
    """

    ID = 'layout-reload'

    def __init__(self):
        super().__init__(
            id=self.ID,
            refresh=True
        )
