import dash_bootstrap_components as dbc
from dash import html


from indizio.components.matrix.parameters.binning_option import MatrixParamsBinningOption
from indizio.components.matrix.parameters.color_scale import MatrixParamsColorScale
from indizio.components.matrix.parameters.color_slider import MatrixParamsColorSlider
from indizio.components.matrix.parameters.metric import MatrixParamsMetric
from indizio.components.matrix.parameters.update_button import MatrixParamsUpdateButton


class MatrixParametersCanvas(dbc.Card):
    """
    This component shows the values that are selected in the NetworkForm component.
    """
    ID = "matrix-parameters-canvas"

    def __init__(self):
        super().__init__(
            children=[
                dbc.CardHeader("Matrix Parameters"),
                dbc.CardBody(
                    children=[
                        dbc.Row(MatrixParamsMetric()),
                        dbc.Row(MatrixParamsColorScale(), className="mt-2"),
                        dbc.Row(MatrixParamsBinningOption(), className="mt-2"),
                        dbc.Row(MatrixParamsColorSlider(), className="mt-2"),
                        dbc.Row(MatrixParamsUpdateButton(), className="mt-2")
                    ]
                )
            ]
        )
