import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, callback

from indizio.components.clustergram.parameters.cluster_on import ClustergramParamsClusterOn
from indizio.components.clustergram.parameters.metadata import ClustergramParamsMetadata
from indizio.components.clustergram.parameters.metric import ClustergramParamsMetric
from indizio.components.clustergram.parameters.optimal_leaf_order import ClustergramParamsOptimalLeafOrder
from indizio.components.clustergram.parameters.sync_with_network import ClustergramParamsSyncWithNetwork
from indizio.components.clustergram.parameters.tree import ClustergramParamsTree
from indizio.components.clustergram.parameters.update_button import ClustergramParamsUpdateButton


class ClustergramParametersCanvas(html.Div):
    """
    This is the main card that wraps the Clustergram parameters.
    """
    ID = "clustergram-parameters-canvas"
    ID_TOGGLE_BTN = f'{ID}-toggle-btn'
    ID_CANVAS = f'{ID}-canvas'

    def __init__(self):
        super().__init__(
            children=[
                dbc.Button(
                    "Clustergram Parameters",
                    id=self.ID_TOGGLE_BTN,
                    n_clicks=0,
                ),
                dbc.Offcanvas(
                    id=self.ID_CANVAS,
                    className="network-properties-container",
                    style={
                        "minWidth": "800px"
                    },
                    scrollable=True,
                    title="Clustergram Parameters",
                    is_open=False,
                    children=[
                        dbc.Row(ClustergramParamsMetric()),
                        dbc.Row(ClustergramParamsTree(), className="mt-2"),
                        dbc.Row(ClustergramParamsMetadata(), className="mt-2"),
                        dbc.Row(ClustergramParamsClusterOn(), className='mt-2'),
                        dbc.Row(ClustergramParamsSyncWithNetwork(), className='mt-2'),
                        dbc.Row(ClustergramParamsOptimalLeafOrder(), className='mt-2'),
                        dbc.Row(ClustergramParamsUpdateButton(), className="mt-2")
                    ]
                ),
            ]
        )

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
