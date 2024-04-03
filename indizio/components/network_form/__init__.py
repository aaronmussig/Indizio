import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, callback

from indizio.components.network_form.btn_update import NetworkFormBtnUpdate
from indizio.components.network_form.degree import NetworkFormDegree
from indizio.components.network_form.layout import NetworkFormLayout
from indizio.components.network_form.node_metadata import NetworkFormNodeMetadata
from indizio.components.network_form.node_of_interest import NetworkFormNodeOfInterest
from indizio.components.network_form.thresh_filter_container import NetworkThreshFilterContainer


class NetworkFormParameters(html.Div):
    """
    This class wraps the network form.
    """
    ID = 'network-form'
    ID_TOGGLE_BTN = f'{ID}-toggle-btn'
    ID_CANVAS = f'{ID}-canvas'

    def __init__(self):
        super().__init__(
            children=[
                dbc.Button(
                    "Network Parameters",
                    id=self.ID_TOGGLE_BTN,
                    n_clicks=0,
                ),
                dbc.Offcanvas(
                    id=self.ID_CANVAS,
                    className="network-properties-container",
                    scrollable=True,
                    title="Network Parameters",
                    is_open=False,
                    children=[
                        NetworkFormLayout(),


                        html.Div(
                            className='mt-3',
                            children=[
                                NetworkFormNodeOfInterest(),
                            ]),

                        html.Div(
                            className='mt-3',
                            children=[
                                NetworkFormNodeMetadata(),
                            ]
                        ),

                        html.Div(
                            className='mt-3',
                            children=[
                                NetworkFormDegree(),
                            ]),


                        html.Div(
                            className='mt-3',
                            children=[
                                NetworkThreshFilterContainer(),
                            ]),

                        html.Div(
                            className='mt-3',
                            children=[
                                NetworkFormBtnUpdate(),
                            ])

                    ]
                ),
            ])

        @callback(
            output=dict(
                is_open=Output(self.ID_CANVAS, "is_open"),
            ),
            inputs=dict(
                n1=Input(self.ID_TOGGLE_BTN, "n_clicks"),
                is_open=State(self.ID_CANVAS, "is_open"),
            ),
        )
        def toggle_network_form(n1, is_open):
            open_form = False
            if n1:
                open_form = not is_open
            return dict(
                is_open=open_form
            )
