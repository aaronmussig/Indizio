import dash_bootstrap_components as dbc


class DownloadGraphMlButton(dbc.Button):
    """
    This component is the "Download as GraphML" button.
    """

    ID = "download-graphml-button"

    def __init__(self):
        super().__init__(
            "Download as GraphML",
            id=self.ID,
            color="success"
        )
