import logging
from typing import List, Dict, Optional

import dash_cytoscape as cyto
import plotly.express as px
from dash import Output, Input, callback, State, html
from dash.exceptions import PreventUpdate

from indizio.config import ID_NETWORK_VIZ_NODE_EDGE_COUNT
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.metadata_file import MetadataFileStore, MetadataData
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData, NetworkParamNodeSize, \
    NetworkParamNodeColor
from indizio.store.network_interaction import NetworkInteractionStore, NetworkInteractionData
from indizio.util.data import is_numeric
from indizio.util.plot import numerical_colorscale


class NetworkVizStyleSheet:
    DEFAULT = {
        "node": {
            "width": "mapData(size, 0, 100, 15, 80)",
            "height": "mapData(size, 0, 100, 15, 80)",
            "background-color": "data(color)",
            "content": "data(label)",
        },
        "edge": {
            "opacity": 0.4
        },
    }

    def __init__(self, data=None):
        self.data = {**self.DEFAULT, **(data or {})}

    @classmethod
    def from_graph(cls, stylesheet):
        out = dict()
        for item in stylesheet:
            out[item['selector']] = item['style']
        return cls(out)

    def node_selected_key(self, node_id: str) -> str:
        return f'node[id = "{node_id}"]'

    def edge_selected_key(self, edge_id: str) -> str:
        return f'edge[id = "{edge_id}"]'

    def has_node_selected(self, node_id: str) -> bool:
        return self.node_selected_key(node_id) in self.data

    def set_node_id_toggled(self, node_id: str):
        node_key = self.node_selected_key(node_id)
        new_data = {
            "background-color": "#eb6864",
            "border-color": "#963835",
            "border-width": 2,
            "border-opacity": 1,
            "opacity": 1,
            # "color": "#963835",
            "text-opacity": 1,
            # "font-size": 16,
            "z-index": 9999,
        }
        self.data[node_key] = {**self.data.get(node_key, dict()), **new_data}

    def set_edge_id_toggled(self, edge_id: str):
        edge_key = self.edge_selected_key(edge_id)
        new_data = {
            "line-color": "#eb6864",
            "opacity": 0.9,
            "z-index": 9000,
        }
        self.data[edge_key] = {**self.data.get(edge_key, dict()), **new_data}

    def export(self) -> List[Dict]:
        out = list()
        for selector, style in self.data.items():
            out.append({
                'selector': selector,
                'style': style
            })
        return out


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
                    stylesheet=NetworkVizStyleSheet().export()
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
                state_meta=State(MetadataFileStore.ID, "data"),
            ),
            running=[
                (Output(self.ID_GRAPH, 'style'), {'visibility': 'hidden'}, {'visibility': 'visible'}),
                (Output(ID_NETWORK_VIZ_NODE_EDGE_COUNT, 'children'), 'Loading...', 'No distance matrix loaded.'),
            ],
            background=True,
        )
        def draw_graph(ts_graph, ts_param, state_graph, state_params, state_meta):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID_GRAPH} - Drawing graph.')
            if ts_graph is None or state_graph is None:
                log.debug(f'{self.ID_GRAPH} - No data to draw graph.')
                raise PreventUpdate

            # Load the data
            graph = DmGraph(**state_graph)
            params = NetworkFormStoreData(**state_params)
            meta = MetadataData(**state_meta)

            out_graph = graph.filter_to_cytoscape(params)

            # If metadata is available, add it to the nodes
            node_sizes = get_sizes_for_nodes(params.node_size, meta)
            node_colors = get_colours_for_nodes(params.node_color, meta)

            # Update the node sizes
            for cur_node in out_graph['nodes']:
                cur_node_data = cur_node['data']
                cur_node_id = cur_node_data['id']

                cur_node_data['size'] = node_sizes.get(cur_node_id, 20)
                cur_node_data['color'] = node_colors.get(cur_node_id, '#848484')

            # Return the graph
            return dict(
                elements=out_graph,
                layout={'name': params.layout.name.replace('_', '-'), 'animate': True},
                node_edge_children=f'Nodes: {len(out_graph["nodes"]):,} | Edges: {len(out_graph["edges"]):,}',
            )

        @callback(
            output=dict(
                stylesheet=Output(self.ID_GRAPH, 'stylesheet'),
                network_interaction=Output(NetworkInteractionStore.ID, 'data')
            ),
            inputs=dict(
                node=Input(self.ID_GRAPH, "tapNode"),
                prev_stylesheet=State(self.ID_GRAPH, 'stylesheet'),
                network_interaction_state=State(NetworkInteractionStore.ID, 'data')
            ),
            prevent_initial_call=True
        )
        def highlight_on_node_select(node, prev_stylesheet, network_interaction_state):
            # Output debugging information
            log = logging.getLogger()
            log.debug(f'{self.ID_GRAPH} - Node clicked.')

            # Load the default stylesheet
            default_stylesheet = NetworkVizStyleSheet()

            # Store this in the network interaction store
            network_interaction_store = NetworkInteractionData(**network_interaction_state)

            # No node is selected, just return the default stylesheet
            if node is None:
                return dict(
                    stylesheet=default_stylesheet.export(),
                    network_interaction=network_interaction_store.model_dump(mode='json')
                )

            # Record this interaction
            network_interaction_store.select_node(node['data']['id'])

            # Check the previous stylesheet to see if the user is clicking
            # the same node again (i.e. deselecting)
            if prev_stylesheet:
                prev_stylesheet_obj = NetworkVizStyleSheet().from_graph(prev_stylesheet)
                if prev_stylesheet_obj.has_node_selected(node['data']['id']):
                    return dict(
                        stylesheet=default_stylesheet.export(),
                        network_interaction=network_interaction_store.model_dump(mode='json')
                    )

            # Otherwise, update the stylesheet with the new node
            default_stylesheet.set_node_id_toggled(node['data']['id'])
            for edge in node["edgesData"]:
                default_stylesheet.set_edge_id_toggled(edge["id"])

            for edge in {x['source'] for x in node["edgesData"]}:
                network_interaction_store.add_edge_node(edge)

            # Export the updated stylesheet with highlighting
            return dict(
                stylesheet=default_stylesheet.export(),
                network_interaction=network_interaction_store.model_dump(mode='json')
            )


def get_sizes_for_nodes(param: Optional[NetworkParamNodeSize], meta: MetadataData):
    # Nothing to do
    if param is None:
        return dict()

    # Read the metadata file
    cur_meta_file = meta.get_file(param.file_id).read()
    cur_row_to_val = cur_meta_file[param.column].dropna().to_dict()

    # Filter those to numeric values only
    cur_row_to_val = {k: v for k, v in cur_row_to_val.items() if is_numeric(v)}
    if not cur_row_to_val:
        return dict()

    # Normalize the values between 0 and 100
    cur_min = min(cur_row_to_val.values())
    cur_max = max(cur_row_to_val.values())
    cur_range = cur_max - cur_min
    cur_row_to_val = {k: (v - cur_min) / cur_range * 100 for k, v in cur_row_to_val.items()}

    # Format the value
    out = dict()
    for cur_node_id, cur_value in cur_row_to_val.items():
        out[cur_node_id] = float(cur_value)

    return out


def get_colours_for_nodes(param: Optional[NetworkParamNodeColor], meta: MetadataData):
    # Nothing to do
    if param is None:
        return dict()

    # Read the metadata file
    cur_meta_file = meta.get_file(param.file_id).read()
    cur_row_to_val = cur_meta_file[param.column].dropna().to_dict()

    # Check if all values are numeric (gradient)
    all_numeric = all(is_numeric(v) for v in cur_row_to_val.values())
    out = dict()

    # All numeric values implies a gradient for those values present
    if all_numeric:

        d_value_to_color = numerical_colorscale(cur_row_to_val.values(), 'inferno')

        for cur_row, cur_val in cur_row_to_val.items():
            out[cur_row] = d_value_to_color[cur_val]

    # Otherwise, use a categorical color scheme
    else:
        categories = sorted(set(cur_row_to_val.values()))

        # Create a unique colour from the Plotly3 colour map for each category
        color_scale = px.colors.qualitative.Dark24
        category_colors = {category: color_scale[i % len(color_scale)] for i, category in enumerate(categories)}

        for cur_row, cur_val in cur_row_to_val.items():
            out[cur_row] = category_colors[cur_val]

    return out
