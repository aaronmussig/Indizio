import dash_bootstrap_components as dbc

NAVBAR = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Matrices", href="/matrix")),
        dbc.NavItem(dbc.NavLink("Network Visualization", href="/network")),
        dbc.NavItem(dbc.NavLink("Network Statistics", href="/stats")),
    ],
    brand="Indizio",
    brand_href="/",
    color="primary",
    dark=True,
)


class NavBar(dbc.NavbarSimple):

    def __init__(self):
        # Define the component's layout
        super().__init__(
            brand='Indizio',
            brand_href='/',
            color="primary",
            dark=True,
            children=[
                dbc.NavItem(dbc.NavLink("Matrices", href="/matrix")),
                dbc.NavItem(dbc.NavLink("Network Visualization", href="/network")),
                dbc.NavItem(dbc.NavLink("Network Statistics", href="/stats")),
            ])

    pass
