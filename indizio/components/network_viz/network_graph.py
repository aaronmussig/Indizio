import logging
from functools import lru_cache

import dash_cytoscape as cyto
from dash import Output, Input, callback, State
from dash.exceptions import PreventUpdate

from indizio.components.network_properties import NetworkPropertiesCard
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData
from indizio.util.cache import freezeargs, from_hashable
from indizio.util.graph import filter_graph


class NetworkVizGraph(cyto.Cytoscape):
    """
    The cytoscape network graph component.
    """

    ID = 'network-viz-graph'

    def __init__(self):
        super().__init__(
            id=self.ID,
            elements=[],
            # stylesheet=stylesheet,
            layout={"name": "grid", 'animate': True},
            style={'width': '100%', 'height': 'calc(100vh - 150px)'},
            responsive=True,
        )

        @callback(
            output=dict(
                elements=Output(self.ID, 'elements'),
                layout=Output(self.ID, "layout"),
                n_nodes=Output(NetworkPropertiesCard.ID_N_NODES, "children"),
                n_edges=Output(NetworkPropertiesCard.ID_N_EDGES, "children"),
            ),
            inputs=dict(
                ts_graph=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                ts_param=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
            ),
        )
        @freezeargs
        @lru_cache
        def draw_graph(ts_graph, ts_param, state_graph, state_params):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID} - Drawing graph.')
            if ts_graph is None or state_graph is None:
                log.debug(f'{self.ID} - No data to draw graph.')
                raise PreventUpdate

            # Networkx mutates the state so it must be de-serialized
            state_graph = from_hashable(state_graph)

            # De-serialize the states
            graph = DmGraph.deserialize(state_graph)
            params = NetworkFormStoreData(**state_params)

            # Filter the graph based on the parameters
            out_graph = filter_graph(
                G=graph.graph,
                node_subset=params.node_of_interest,
                degree=params.thresh_degree,
                thresh=params.corr_input,
                thresh_op=params.thresh_corr_select
            )['elements']

            # There is a formatting quirk with cytoscape that requires a reformat
            # to display the label correctly
            for node in out_graph['nodes']:
                node['data']['label'] = node['data']['name']
                del node['data']['name']

            return dict(
                elements=out_graph,
                layout={'name': params.layout.name, 'animate': True},
                n_nodes=len(out_graph['nodes']),
                n_edges=len(out_graph['edges'])
            )

        @callback(
            output=dict(
                stylesheet=Output(self.ID, 'stylesheet'),
            ),
            inputs=dict(
                node=Input(self.ID, "tapNode"),
                prev_stylesheet=State(self.ID, 'stylesheet'),
            ),
        )
        def highlight_on_node_select(node, prev_stylesheet):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID} - Node clicked.')

            stylesheet = [
                {
                    "selector": "edge",
                    "style": {
                        # 'width': 'mapData(lr, 50, 200, 0.75, 5)',
                        "opacity": 0.4,
                    },
                },
                {
                    "selector": "node",
                    "style": {
                        # 'color': '#317b75',
                        "background-color": "#317b75",
                        "content": "data(label)",
                    },
                },
                {
                    "selector": ".focal",
                    "style": {
                        # 'color': '#E65340',
                        "background-color": "#E65340",
                        "content": "data(label)",
                    },
                },
                {
                    "selector": ".other",
                    "style": {
                        # 'color': '#317b75',
                        "background-color": "#317b75",
                        "content": "data(label)",
                    },
                },
            ]
            if node is None:
                return dict(
                    stylesheet=stylesheet
                )

            # Check the previous stylesheet to see if the user is clicking
            # the same node again (i.e. deselecting)
            if prev_stylesheet is not None:
                for style in prev_stylesheet:
                    if style.get('selector') == 'node[id = "{}"]'.format(node['data']['id']):
                        return dict(
                            stylesheet=stylesheet
                        )

            # Otherwise, update the stylesheet with the new node
            stylesheet = [
                {
                    "selector": "edge",
                    "style": {
                        "opacity": 0.4,
                        # 'width': 'mapData(lr, 50, 200, 0.75, 5)',
                    },
                },
                {
                    "selector": "node",
                    "style": {
                        # 'color': '#317b75',
                        "background-color": "#317b75",
                        "content": "data(label)",
                        "width": "mapData(degree, 1, 100, 25, 200)",
                    },
                },
                {
                    "selector": ".focal",
                    "style": {
                        # 'color': '#E65340',
                        "background-color": "#E65340",
                        "content": "data(label)",
                    },
                },
                {
                    "selector": ".other",
                    "style": {
                        # 'color': '#317b75',
                        "background-color": "#317b75",
                        "content": "data(label)",
                    },
                },
                {
                    "selector": 'node[id = "{}"]'.format(node["data"]["id"]),
                    "style": {
                        "background-color": "#B10DC9",
                        "border-color": "purple",
                        "border-width": 2,
                        "border-opacity": 1,
                        "opacity": 1,
                        "label": "data(label)",
                        "color": "#B10DC9",
                        "text-opacity": 1,
                        "font-size": 12,
                        "z-index": 9999,
                    },
                },
            ]
            for edge in node["edgesData"]:
                stylesheet.append(
                    {
                        "selector": 'node[id= "{}"]'.format(edge["target"]),
                        "style": {
                            "background-color": "blue",
                            "opacity": 0.9,
                        },
                    }
                )
                stylesheet.append(
                    {
                        "selector": 'node[id= "{}"]'.format(edge["source"]),
                        "style": {
                            "background-color": "blue",
                            "opacity": 0.9,
                        },
                    }
                )
                stylesheet.append(
                    {
                        "selector": 'edge[id= "{}"]'.format(edge["id"]),
                        "style": {"line-color": "green", "opacity": 0.9, "z-index": 5000},
                    }
                )
            return dict(
                stylesheet=stylesheet
            )