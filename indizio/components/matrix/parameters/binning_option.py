import dash_bootstrap_components as dbc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.matrix_parameters import MatrixBinOption, MatrixParameters


class MatrixParamsBinningOption(dbc.Row):
    ID = "matrix-params-binning-option"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Aggregation",
                        html_for=self.ID,
                        style={'font-weight': 'bold'}
                    ),
                    width=3
                ),
                dbc.Col(
                    dbc.RadioItems(
                        options=MatrixBinOption.to_options(),
                        value=MatrixParameters().bin_option.value,
                        id=self.ID,
                        inline=True,
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE

                    )
                )
            ]
        )
