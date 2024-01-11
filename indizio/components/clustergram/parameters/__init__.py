import dash_bootstrap_components as dbc
from dash import html

from indizio.components.clustergram.parameters.metadata import ClustergramParamsMetadata
from indizio.components.clustergram.parameters.metric import ClustergramParamsMetric
from indizio.components.clustergram.parameters.tree import ClustergramParamsTree
from indizio.components.clustergram.parameters.update_button import ClustergramParamsUpdateButton
from indizio.components.matrix.parameters.binning_option import MatrixParamsBinningOption
from indizio.components.matrix.parameters.color_scale import MatrixParamsColorScale
from indizio.components.matrix.parameters.color_slider import MatrixParamsColorSlider
from indizio.components.matrix.parameters.metric import MatrixParamsMetric
from indizio.components.matrix.parameters.update_button import MatrixParamsUpdateButton


class ClustergramParametersCanvas(dbc.Card):
    """
    This component shows the values that are selected in the NetworkForm component.
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
                        # dbc.Row(MatrixParamsBinningOption(), className="mt-2"),
                        # dbc.Row(MatrixParamsColorSlider(), className="mt-2"),
                        dbc.Row(ClustergramParamsUpdateButton(), className="mt-2")
                    ]
                )
            ]
        )
