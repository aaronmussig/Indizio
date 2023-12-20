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

        # @callback(
        #     output=dict(
        #         options=Output(self.ID, "options"),
        #     ),
        #     inputs=dict(
        #         ts=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
        #         state=State(DistanceMatrixGraphStore.ID, "data"),
        #     )
        # )
        # def update_options_on_file_upload(ts, state):
        #     log = logging.getLogger()
        #     log.debug(f'{self.ID} - Updating the nodes of interest selection from user file update.')
        #
        #     if ts is None or state is None:
        #         log.debug(f'{self.ID} - No data to update from.')
        #         raise PreventUpdate
        #
        #     # De-serialize the graph and return the nodes
        #     graph = DmGraph.deserialize(state)
        #     return dict(
        #         options=[x for x in graph.graph.nodes]
        #     )
