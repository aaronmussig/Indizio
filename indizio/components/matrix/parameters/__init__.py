import dash_bootstrap_components as dbc
from dash import html

from indizio.components.matrix.parameters.color_range import MatrixParamsColorRange
from indizio.components.matrix.parameters.color_scale import MatrixParamsColorScale
from indizio.components.matrix.parameters.metric import MatrixParamsMetric
from indizio.components.matrix.parameters.sync_with_network import MatrixParamsSyncWithNetwork
from indizio.components.matrix.parameters.update_button import MatrixParamsUpdateButton


class MatrixParametersCanvas(dbc.Card):
    """
    This component contains the matrix parameters.
    """
    ID = "matrix-parameters-canvas"

    def __init__(self):
        super().__init__(
            children=[
                dbc.CardHeader(html.H5("Matrix Parameters")),
                dbc.CardBody(
                    children=[
                        dbc.Row(MatrixParamsMetric()),
                        dbc.Row(MatrixParamsColorScale(), className="mt-2"),
                        dbc.Row(MatrixParamsColorRange(), className='mt-2'),
                        dbc.Row(MatrixParamsSyncWithNetwork(), className='mt-2'),
                        dbc.Row(MatrixParamsUpdateButton(), className="mt-2")
                    ]
                )
            ]
        )
