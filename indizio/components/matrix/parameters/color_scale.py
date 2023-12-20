import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc

from indizio.config import PERSISTENCE_TYPE
from indizio.store.matrix_parameters import MatrixParameters


class MatrixParamsColorScale(dbc.Row):
    ID = "matrix-params-color-scale"

    def __init__(self):
        super().__init__(
            [
                dbc.Col(
                    dbc.Label(
                        "Color scale",
                        html_for=self.ID,
                        style={'font-weight': 'bold'}
                    ),
                    width=3,
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id=self.ID,
                        options=px.colors.named_colorscales(),
                        value=MatrixParameters().color_scale,
                        className="bg-light text-dark",
                        persistence=True,
                        persistence_type=PERSISTENCE_TYPE
                    )
                )
            ]
        )
