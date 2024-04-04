import dash_bootstrap_components as dbc
from dash import html

from indizio.components.clustergram.parameters.cluster_on import ClustergramParamsClusterOn
from indizio.components.clustergram.parameters.metadata import ClustergramParamsMetadata
from indizio.components.clustergram.parameters.metric import ClustergramParamsMetric
from indizio.components.clustergram.parameters.optimal_leaf_order import ClustergramParamsOptimalLeafOrder
from indizio.components.clustergram.parameters.tree import ClustergramParamsTree
from indizio.components.clustergram.parameters.update_button import ClustergramParamsUpdateButton


class ClustergramParametersCanvas(dbc.Card):
    """
    This is the main card that wraps the Clustergram parameters.
    """
    ID = "clustergram-parameters-canvas"

    def __init__(self):
        super().__init__(
            children=[
                dbc.CardHeader(html.H5("Clustergram Parameters")),
                dbc.CardBody(
                    children=[
                        dbc.Row(ClustergramParamsMetric()),
                        dbc.Row(ClustergramParamsTree(), className="mt-2"),
                        dbc.Row(ClustergramParamsMetadata(), className="mt-2"),
                        dbc.Row(ClustergramParamsClusterOn(), className='mt-2'),
                        dbc.Row(ClustergramParamsOptimalLeafOrder(), className='mt-2'),
                        dbc.Row(ClustergramParamsUpdateButton(), className="mt-2")
                    ]
                )
            ]
        )
