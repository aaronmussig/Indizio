import dash_bootstrap_components as dbc
from dash import Output, Input, callback

from indizio import __version__
from indizio.store.matrix.dm_files import DistanceMatrixStore, DistanceMatrixStoreModel
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceStoreModel


class NavBar(dbc.NavbarSimple):
    """
    This component is the default Navigation bar shown on all pages.
    """

    ID = 'navbar-container'

    ID_MATRIX = f'{ID}-matrix'
    ID_NETWORK = f'{ID}-network'
    ID_CLUSTERGRAM = f'{ID}-clustergram'
    ID_DEBUG = f'{ID}-debug'

    ID_MATRIX_CONTAINER = f'{ID_MATRIX}-container'
    ID_NETWORK_CONTAINER = f'{ID_NETWORK}-container'
    ID_CLUSTERGRAM_CONTAINER = f'{ID_CLUSTERGRAM}-container'

    ID_MATRIX_TOOLTIP = f'{ID_MATRIX}-tooltip'
    ID_NETWORK_TOOLTIP = f'{ID_NETWORK}-tooltip'
    ID_CLUSTERGRAM_TOOLTIP = f'{ID_CLUSTERGRAM}-tooltip'

    def __init__(self, debug: bool):
        children = [
            dbc.NavItem(
                id=self.ID_MATRIX_CONTAINER,
                children=[
                    dbc.NavLink(
                        "Matrices",
                        href="/matrix",
                        disabled=False,
                        id=self.ID_MATRIX
                    ),
                    dbc.Tooltip(
                        "A presence/absence, or distance matrix is required.",
                        id=self.ID_MATRIX_TOOLTIP,
                        target=self.ID_MATRIX_CONTAINER,
                        placement='bottom',
                    )
                ]
            ),
            dbc.NavItem(
                id=self.ID_NETWORK_CONTAINER,
                children=[
                    dbc.NavLink(
                        "Network Visualization",
                        href="/network",
                        disabled=False,
                        id=self.ID_NETWORK
                    ),
                    dbc.Tooltip(
                        "A presence/absence, or distance matrix is required.",
                        id=self.ID_NETWORK_TOOLTIP,
                        target=self.ID_NETWORK_CONTAINER,
                        placement='bottom',
                    )
                ]
            ),
            dbc.NavItem(
                id=self.ID_CLUSTERGRAM_CONTAINER,
                children=[
                    dbc.NavLink(
                        "Clustergram",
                        href="/clustergram",
                        disabled=False,
                        id=self.ID_CLUSTERGRAM
                    ),
                    dbc.Tooltip(
                        "A presence/absence matrix is required.",
                        id=self.ID_CLUSTERGRAM_TOOLTIP,
                        target=self.ID_CLUSTERGRAM_CONTAINER,
                        placement='bottom',
                    )
                ]
            )
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
                matricies=Output(self.ID_MATRIX, 'disabled'),
                matricies_tip_style=Output(self.ID_MATRIX_TOOLTIP, 'style'),
                network=Output(self.ID_NETWORK, 'disabled'),
                network_tip_style=Output(self.ID_NETWORK_TOOLTIP, 'style'),
                clustergram=Output(self.ID_CLUSTERGRAM, 'disabled'),
                clustergram_tip_style=Output(self.ID_CLUSTERGRAM_TOOLTIP, 'style'),
            ),
            inputs=dict(
                state_dm=Input(DistanceMatrixStore.ID, 'data'),
                state_pa=Input(PresenceAbsenceStore.ID, 'data'),
            ),
        )
        def toggle_nav_disabled(state_dm, state_pa):
            state_dm = DistanceMatrixStoreModel(**state_dm)
            state_pa = PresenceAbsenceStoreModel(**state_pa)

            disabled_style = {'visibility': 'hidden'}

            no_dist_matrix = state_dm.n_files() == 0
            no_pa_matrix = state_pa.n_files() == 0
            return dict(
                matricies=no_dist_matrix,
                matricies_tip_style={} if no_dist_matrix and no_pa_matrix else disabled_style,
                network=no_dist_matrix,
                network_tip_style={} if no_dist_matrix and no_pa_matrix else disabled_style,
                clustergram=no_pa_matrix,
                clustergram_tip_style={} if no_pa_matrix else disabled_style,
            )
