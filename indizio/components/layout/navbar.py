import dash_bootstrap_components as dbc
from dash import Output, Input, callback

from indizio import __version__
from indizio.store.matrix.dm_files import DistanceMatrixStore


class NavBar(dbc.NavbarSimple):
    """
    This component is the default Navigation bar shown on all pages.
    """

    ID = 'navbar-container'
    ID_MATRIX = f'{ID}-matrix'
    ID_VIZ = f'{ID}-viz'
    ID_STATS = f'{ID}-stats'
    ID_DEBUG = f'{ID}-debug'

    def __init__(self, debug: bool):
        children = [
            dbc.NavItem(dbc.NavLink(
                "Matrices",
                href="/matrix",
                disabled=False,
                id=self.ID_MATRIX
            )),
            dbc.NavItem(dbc.NavLink(
                "Network Visualization",
                href="/network",
                id=self.ID_VIZ
            )),
            dbc.NavItem(dbc.NavLink(
                "Clustergram",
                href="/clustergram",
                id=self.ID_STATS
            ))
        ]
        if debug:
            children.append(
                dbc.NavItem(dbc.NavLink(
                    "Debug",
                    href="/debug",
                    id=self.ID_DEBUG
                ))
            )

        super().__init__(
            brand=[
                'Indizio',
                dbc.Badge(
                    pill=True,
                    children=f'v{__version__}',
                    color='#ed9390',
                    style={
                        'marginLeft': '5px',
                        'fontSize': '10px',
                    }
                )
            ],
            brand_href='/',
            color="primary",
            dark=True,
            children=children)

        @callback(
            output=dict(
                matrix=Output(self.ID_MATRIX, 'disabled'),
                viz=Output(self.ID_VIZ, 'disabled'),
                stats=Output(self.ID_STATS, 'disabled')
            ),
            inputs=dict(
                state_dm=Input(DistanceMatrixStore.ID, 'data'),
            ),
        )
        def toggle_nav_disabled(state_dm):
            disabled = not state_dm
            return dict(
                matrix=disabled,
                viz=disabled,
                stats=disabled
            )
