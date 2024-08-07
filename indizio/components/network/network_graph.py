from typing import Optional

import dash_cytoscape as cyto
import plotly.express as px
from dash import Output, Input, callback, State, dcc
from dash.exceptions import PreventUpdate

from indizio.config import ID_NETWORK_VIZ_EDGE_COUNT, ID_NETWORK_VIZ_NODE_COUNT, ID_NETWORK_VIZ_FILTERING_APPLIED
from indizio.models.network.parameters import EdgeWeights, NetworkParamNodeColor, NetworkParamNodeSize
from indizio.models.network.stylesheet import NetworkVizStyleSheet
from indizio.store.metadata_file import MetadataFileStore, MetadataFileStoreModel
from indizio.store.network.graph import DistanceMatrixGraphStore, DistanceMatrixGraphStoreModel
from indizio.store.network.interaction import NetworkInteractionStoreModel, NetworkInteractionStore
from indizio.store.network.parameters import NetworkFormStore, NetworkFormStoreModel
from indizio.util.data import is_numeric
from indizio.util.log import log_debug
from indizio.util.plot import numerical_colorscale


class NetworkVizGraph(dcc.Loading):
    """
    The cytoscape network graph component.
    """
    ID = 'network-viz-graph'
    ID_GRAPH = f'{ID}-cytoscape'
    ID_LOADING = f'{ID}-loading'

    def __init__(self):
        super().__init__(
            id=self.ID_LOADING,
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
                edge_count=Output(ID_NETWORK_VIZ_EDGE_COUNT, 'children'),
                node_count=Output(ID_NETWORK_VIZ_NODE_COUNT, 'children'),
                filtering=Output(ID_NETWORK_VIZ_FILTERING_APPLIED, 'style'),
                stylesheet=Output(self.ID_GRAPH, 'stylesheet'),
            ),
            inputs=dict(
                ts_graph=Input(DistanceMatrixGraphStore.ID, "modified_timestamp"),
                ts_param=Input(NetworkFormStore.ID, "modified_timestamp"),
                state_graph=State(DistanceMatrixGraphStore.ID, "data"),
                state_params=State(NetworkFormStore.ID, "data"),
                state_meta=State(MetadataFileStore.ID, "data"),
                prev_stylesheet=State(self.ID_GRAPH, 'stylesheet'),
                network_interaction_state=State(NetworkInteractionStore.ID, 'data')
            ),
        )
        def draw_graph(ts_graph, ts_param, state_graph, state_params, state_meta, prev_stylesheet,
                       network_interaction_state):
            # Output debugging information
            log_debug(f'{self.ID_GRAPH} - Drawing graph.')
            if ts_graph is None or state_graph is None:
                log_debug(f'{self.ID_GRAPH} - No data to draw graph.')
                raise PreventUpdate

            # Load the data
            graph = DistanceMatrixGraphStoreModel(**state_graph)
            graph_read = graph.read()
            params = NetworkFormStoreModel(**state_params)
            meta = MetadataFileStoreModel(**state_meta)
            interact = NetworkInteractionStoreModel(**network_interaction_state)

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

            # Calculate how many nodes are visible
            n_nodes_vis = len(out_graph['nodes'])
            n_nodes_tot = len(graph_read.nodes)
            n_edges_vis = len(out_graph['edges'])
            n_edges_tot = len(graph_read.edges)

            # Toggle the filtering warning based on the graph counts
            if n_nodes_tot != n_nodes_vis or n_edges_tot != n_edges_vis:
                filtering = 'visible'
            else:
                filtering = 'hidden'

            # Add a label to each edge if the user has requested it
            stylesheet = NetworkVizStyleSheet().from_graph(
                prev_stylesheet) if prev_stylesheet else NetworkVizStyleSheet()

            # Reflect the state of the interaction in the stylesheet
            stylesheet.update_from_iteraction_store(interact, out_graph.get('edges', list()))

            if params.edge_weights is not None:

                show_edge_text = params.edge_weights.value is EdgeWeights.TEXT or params.edge_weights.value is EdgeWeights.BOTH
                show_edge_width = params.edge_weights.value is EdgeWeights.WEIGHT or params.edge_weights.value is EdgeWeights.BOTH

                # Enable the label in the stylesheet
                if show_edge_text:
                    stylesheet.enable_edge_weights_text()
                else:
                    stylesheet.disable_edge_weights_text()

                if show_edge_width:
                    stylesheet.enable_edge_weights_thick()
                    normed_weights = normalize_edge_weights(
                        params.edge_weights.file_id, list(graph_read.edges.items())
                    )
                else:
                    stylesheet.disable_edge_weights_thick()

                # Iterate over each edge to add the required label (if present)
                for i, cur_edge in enumerate(out_graph['edges']):
                    cur_edge_data = cur_edge['data']

                    if show_edge_text:
                        cur_edge_data['label'] = cur_edge_data.get(params.edge_weights.file_id, 'N/A')

                    if show_edge_width:
                        cur_source = cur_edge_data['source']
                        cur_target = cur_edge_data['target']
                        cur_key = sorted([f'{cur_source}-{cur_target}', f'{cur_target}-{cur_source}'])[0]
                        cur_edge_data['width'] = normed_weights[cur_key]

            # Otherwise, hide the annotations
            else:
                stylesheet.disable_edge_weights_text()
                stylesheet.disable_edge_weights_thick()

            # Return the graph
            return dict(
                elements=dict(out_graph),
                layout={'name': params.layout.name.replace('_', '-'), 'animate': True},
                edge_count=f'Edges: {n_edges_vis:,} / {n_edges_tot:,}',
                node_count=f'Nodes: {n_nodes_vis:,} / {n_nodes_tot:,}',
                filtering={'visibility': filtering},
                stylesheet=stylesheet.export()
            )

        @callback(
            output=dict(
                network_interaction=Output(NetworkInteractionStore.ID, 'data', allow_duplicate=True)
            ),
            inputs=dict(
                graph=Input(self.ID_GRAPH, "elements"),
                state=State(NetworkInteractionStore.ID, 'data')
            ),
            prevent_initial_call=True
        )
        def update_interaction_on_graph_load(graph, state):
            """
            Update the network interaction data based on node selection, or
            what is currently visible.
            """
            if not graph:
                raise PreventUpdate

            # For some reason the graph can either be a dict or list
            if isinstance(graph, dict):
                nodes_visible = {x['data']['id'] for x in graph['nodes']}
            elif isinstance(graph, list):
                nodes_visible = {x['data']['id'] for x in graph}
            else:
                raise PreventUpdate

            # Store this in the network interaction store
            network_interaction_store = NetworkInteractionStoreModel(**state)
            network_interaction_store.set_visible_nodes(nodes_visible)

            # Export the updated stylesheet with highlighting
            return dict(
                network_interaction=network_interaction_store.model_dump(mode='json')
            )

        @callback(
            output=dict(
                network_interaction=Output(NetworkInteractionStore.ID, 'data')
            ),
            inputs=dict(
                node_input=Input(self.ID_GRAPH, "tapNode"),
                graph=State(self.ID_GRAPH, "elements"),
                state=State(NetworkInteractionStore.ID, 'data')
            ),
            prevent_initial_call=True
        )
        def update_interaction_on_node_select(graph, node_input, state):
            """
            Update the network interaction data based on node selection, or
            what is currently visible.
            """
            if not graph:
                raise PreventUpdate

            # For some reason the graph can either be a dict or list
            if isinstance(graph, dict):
                nodes_visible = {x['data']['id'] for x in graph['nodes']}
            elif isinstance(graph, list):
                nodes_visible = {x['data']['id'] for x in graph}
            else:
                raise PreventUpdate

            # Store this in the network interaction store
            network_interaction_store = NetworkInteractionStoreModel(**state)
            network_interaction_store.set_visible_nodes(nodes_visible)

            # Update on node selection
            if node_input is not None:
                # Obtain the node id that was selected
                node_id = node_input['data']['id']

                # Record this interaction
                network_interaction_store.toggle_node(node_id)

            # Export the updated stylesheet with highlighting
            return dict(
                network_interaction=network_interaction_store.model_dump(mode='json')
            )

        @callback(
            output=dict(
                stylesheet=Output(self.ID_GRAPH, 'stylesheet', allow_duplicate=True),
            ),
            inputs=dict(
                network_interaction_ts=Input(NetworkInteractionStore.ID, "modified_timestamp"),
                prev_stylesheet=State(self.ID_GRAPH, 'stylesheet'),
                network_interaction_state=State(NetworkInteractionStore.ID, 'data'),
                graph=State(self.ID_GRAPH, 'elements')
            ),
            prevent_initial_call=True
        )
        def highlight_on_node_select(network_interaction_ts, prev_stylesheet, network_interaction_state, graph):
            # No node is selected
            if network_interaction_ts is None:
                raise PreventUpdate

            # Load the default stylesheet
            stylesheet = NetworkVizStyleSheet().from_graph(prev_stylesheet) \
                if prev_stylesheet else NetworkVizStyleSheet()

            # Load the selected nodes from the store
            network_interaction_store = NetworkInteractionStoreModel(**network_interaction_state)

            # Reflect the state of the interaction in the stylesheet
            # For some reason the graph can either be a dict or list
            if isinstance(graph, dict):
                graph_edges = graph.get('edges', list())
            elif isinstance(graph, list):
                graph_edges = [x for x in graph if 'source' in x.get('data', dict())]
            else:
                raise PreventUpdate

            stylesheet.update_from_iteraction_store(
                network_interaction_store,
                graph_edges
            )

            # Export the updated stylesheet with highlighting
            return dict(
                stylesheet=stylesheet.export(),
            )


def get_sizes_for_nodes(param: Optional[NetworkParamNodeSize], meta: MetadataFileStoreModel):
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


def get_colours_for_nodes(param: Optional[NetworkParamNodeColor], meta: MetadataFileStoreModel):
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


def normalize_edge_weights(file_id, edges):
    data = dict()
    for (source, target), d_values in edges:
        key = sorted([f'{source}-{target}', f'{target}-{source}'])[0]
        value = d_values.get(file_id, 0)
        data[key] = value
    min_val = min(data.values())
    max_val = max(data.values())
    range_val = max_val - min_val
    return {k: (v - min_val) / range_val for k, v in data.items()}
