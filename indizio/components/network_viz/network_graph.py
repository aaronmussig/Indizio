import logging

import dash_cytoscape as cyto
from dash import Output, Input, callback, State, html
from dash.exceptions import PreventUpdate

from indizio.config import ID_NETWORK_VIZ_NODE_EDGE_COUNT
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData


class NetworkVizGraph(html.Div):
    """
    The cytoscape network graph component.
    """
    ID = 'network-viz-graph'
    ID_GRAPH = f'{ID}-cytoscape'

    def __init__(self):
        super().__init__(
            children=[
                cyto.Cytoscape(
                    id=self.ID_GRAPH,
                    elements=[],
                    layout={"name": "grid", 'animate': True},
                    style={'width': '100%', 'height': 'calc(100vh - 210px)'},
                    responsive=True,
                )
            ],
        )

        @callback(
            output=dict(
                elements=Output(self.ID_GRAPH, 'elements'),
                layout=Output(self.ID_GRAPH, "layout"),
                node_edge_children=Output(ID_NETWORK_VIZ_NODE_EDGE_COUNT, 'children'),
            ),
            inputs=dict(
                ts_graph=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                ts_param=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
            ),
            running=[
                (Output(self.ID_GRAPH, 'style'), {'visibility': 'hidden'}, {'visibility': 'visible'}),
                (Output(ID_NETWORK_VIZ_NODE_EDGE_COUNT, 'children'), 'Loading...', 'No distance matrix loaded.'),
            ],
            prevent_initial_call=False,
            background=True,
        )
        def draw_graph(ts_graph, ts_param, state_graph, state_params):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID_GRAPH} - Drawing graph.')
            if ts_graph is None or state_graph is None:
                log.debug(f'{self.ID_GRAPH} - No data to draw graph.')
                raise PreventUpdate

            graph = DmGraph(**state_graph)
            params = NetworkFormStoreData(**state_params)

            out_graph = graph.filter_to_cytoscape(params)

            return dict(
                elements=out_graph,
                layout={'name': params.layout.name.replace('_', '-'), 'animate': True},
                node_edge_children=f'Nodes: {len(out_graph["nodes"]):,} | Edges: {len(out_graph["edges"]):,}'
            )

        @callback(
            output=dict(
                stylesheet=Output(self.ID_GRAPH, 'stylesheet'),
            ),
            inputs=dict(
                node=Input(self.ID_GRAPH, "tapNode"),
                prev_stylesheet=State(self.ID_GRAPH, 'stylesheet'),
            ),
        )
        def highlight_on_node_select(node, prev_stylesheet):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID_GRAPH} - Node clicked.')

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
