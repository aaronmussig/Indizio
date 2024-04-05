import dash_bootstrap_components as dbc
from dash import html

from indizio.components.matrix.matrix_plot import MatrixPlot
from indizio.components.matrix.parameters import MatrixParametersCanvas


class MatrixContainer(dbc.Card):
    """
    This is the container for the matrix plot.
    """

    ID = 'matrix-container'

    def __init__(self):
        super().__init__(
            [
                dbc.CardHeader(html.H5('Matrix')),
                dbc.CardBody(
                    className='p-0',
                    children=[
                        MatrixPlot()
                    ]
                )
            ]
        )
