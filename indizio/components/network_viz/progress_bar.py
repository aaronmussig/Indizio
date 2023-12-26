import dash_bootstrap_components as dbc

from indizio.config import ID_NETWORK_VIZ_PROGRESS


class NetworkVizProgressBar(dbc.Progress):
    """
    The cytoscape network graph component.
    """

    ID = ID_NETWORK_VIZ_PROGRESS

    def __init__(self):
        super().__init__(
            id=self.ID,
            min=0,
            max=100,
            value=100,
            striped=True,
            animated=True,
            style={'visibility': 'hidden'}
        )
