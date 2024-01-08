import dash_bootstrap_components as dbc


class NavBar(dbc.NavbarSimple):

    def __init__(self):
        super().__init__(
            brand='Indizio',
            brand_href='/',
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Matrices", href="/matrix", disabled=False)),
                dbc.NavItem(dbc.NavLink("Network Visualization", href="/network")),
                dbc.NavItem(dbc.NavLink("Network Statistics", href="/stats")),
            ])
