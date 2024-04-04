import dash_bootstrap_components as dbc

from indizio.components.matrix.matrix_plot import MatrixPlot
from indizio.components.matrix.parameters import MatrixParametersCanvas


class MatrixContainer(dbc.Row):
    """
    This is the container for the matrix plot.
    """

    ID = 'matrix-container'

    def __init__(self):
        super().__init__(
            [
                MatrixPlot()
            ]
        )
