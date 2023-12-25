from datetime import datetime

import dash_bootstrap_components as dbc
import networkx as nx
from dash import Output, Input, callback, html, dcc, State
from dash.exceptions import PreventUpdate

from indizio.cache import CACHE_MANAGER
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData
from indizio.util.graph import filter_graph


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
                    color="success"
                ),
                dcc.Download(id=self.ID_DOWNLOAD)
            ]
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
            background=True,
            manager=CACHE_MANAGER
        )
        def on_click(n_clicks, state_graph, state_params):
            if not n_clicks:
                raise PreventUpdate

            # De-serialize the states
            graph = DmGraph(**state_graph).read()
            params = NetworkFormStoreData(**state_params)

            # Filter the graph based on the parameters
            filtered_graph = filter_graph(
                G=graph,
                node_subset=params.node_of_interest,
                degree=params.thresh_degree,
                thresh=params.corr_input,
                thresh_op=params.thresh_corr_select,
            )

            # Convert the graph to GraphML and format the output
            graphml_str = '\n'.join(nx.generate_graphml(filtered_graph))
            date_string = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
            file_name = f'indizio-graph-{date_string}.graphml'

            # Return the data
            return dict(
                dl=dict(content=graphml_str, filename=file_name)
            )
