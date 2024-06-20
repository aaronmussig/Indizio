from datetime import datetime

import dash_bootstrap_components as dbc
import networkx as nx
from dash import Output, Input, callback, html, dcc, State
from dash.exceptions import PreventUpdate

from indizio.store.network.graph import DistanceMatrixGraphStore, DistanceMatrixGraphStoreModel
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel


class DownloadGraphMlButton(html.Div):
    """
    This component is the "Download as GraphML" button.
    """

    ID = "download-graphml-button"
    ID_DOWNLOAD = f'{ID}-download'

    def __init__(self):
        super().__init__(
            [
                dbc.Button(
                    "Download as GraphML",
                    id=self.ID,
                    color="primary"
                ),
                dcc.Download(id=self.ID_DOWNLOAD),
            ],
            style={'marginLeft': '10px'}
        )

        @callback(
            output=dict(
                dl=Output(self.ID_DOWNLOAD, "data"),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
            ),
            running=[
                (Output(self.ID, "disabled"), True, False),
            ],
            prevent_initial_call=True,
            background=False,
        )
        def on_click(n_clicks, state_graph, state_params):
            if not n_clicks:
                raise PreventUpdate

            # De-serialize the states
            graph = DistanceMatrixGraphStoreModel(**state_graph)
            params = NetworkFormStoreModel(**state_params)

            filtered_graph = graph.filter(params)

            # Convert the graph to GraphML and format the output
            graphml_str = '\n'.join(nx.generate_graphml(filtered_graph))
            date_string = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
            file_name = f'indizio-graph-{date_string}.graphml'

            # Return the data
            return dict(
                dl=dict(content=graphml_str, filename=file_name)
            )
