from collections import defaultdict
from pathlib import Path
from typing import List, Collection

import networkx as nx
from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE, TMP_DIR
from indizio.models.common.boolean import BooleanAllAny, BooleanShowHide
from indizio.models.common.bound import Bound
from indizio.models.distance_matrix.dm_file import DistanceMatrixFile
from indizio.store.network.parameters import NetworkFormStoreModel
from indizio.util.dataframe import dataframe_to_pairs
from indizio.util.files import to_pickle, from_pickle
from indizio.util.hashing import calc_md5


class DistanceMatrixGraphStoreModel(BaseModel):
    """
    This is the actual model for the distance matrix graph.
    """
    path: Path
    matrices: List[DistanceMatrixFile]
    hash: str

    @classmethod
    def from_distance_matricies(cls, matrices: Collection[DistanceMatrixFile]):
        """
        Create a graph from a collection of distance matrices.
        """

        # Process each distance matrix file and add the data to the graph
        all_nodes = set()
        all_edges = defaultdict(lambda: defaultdict(dict))
        for dm in matrices:

            # Read the distance matrix
            df = dm.read()

            # Update the nodes seen
            all_nodes.update(set(df.index))

            # Extract the pairwise values from the upper triangle
            df_edge_pairs = dataframe_to_pairs(df)
            for key, value in df_edge_pairs.items():
                # Sort the keys to ensure that a/b is always used instead of b/a
                key_a, key_b = sorted(key)
                all_edges[key_a][key_b][dm.file_id] = value

        # Construct the graph
        G = nx.Graph()
        G.add_nodes_from(sorted(all_nodes))
        for key_a, edge_dict in all_edges.items():
            for key_b, edge_attr_dict in edge_dict.items():
                G.add_edge(key_a, key_b, **edge_attr_dict)

        # Write the graph to disk
        path, md5 = to_pickle(G)

        # Return the object
        return cls(path=path, matrices=matrices, hash=md5)

    def read(self) -> nx.Graph:
        return from_pickle(self.path)

    def filter(self, params: NetworkFormStoreModel):

        # Generate a unique key for the parameters
        param_cache_key = params.get_cache_key()
        combined_cache_key = calc_md5(self.hash.encode() + param_cache_key)
        cache_key = f'cyto-graph-{combined_cache_key}'
        cache_path = TMP_DIR / cache_key

        # Check if this is already present in the cache, if it is then load it
        if cache_path.exists():
            return from_pickle(cache_path)

        # No existing data were found, compute it
        G = self.read()

        # Extract all edges for procesing
        # Filter the nodes if specified
        nodes_to_keep = params.node_of_interest if params.node_of_interest else list(G.nodes)
        edges_to_process = G.edges(nodes_to_keep, data=True)

        # Iterate over each edge and filter them based on the thresholding
        edges_to_keep = list()
        for idx, (edge_from, edge_to, d_edge_data) in enumerate(edges_to_process):

            # Skip edges from self if applicable
            if params.show_edges_to_self is BooleanShowHide.HIDE:
                if edge_from == edge_to:
                    continue

            # Process each metric used to construct the edge to check bounds
            edge_matches = list()
            for file_id, corr in d_edge_data.items():
                cur_threshold = params.thresholds[file_id]

                meets_lower = False
                if cur_threshold.left_bound is Bound.INCLUSIVE:
                    meets_lower = corr >= cur_threshold.left_value
                elif cur_threshold.left_bound is Bound.EXCLUSIVE:
                    meets_lower = corr > cur_threshold.left_value

                meets_upper = False
                if cur_threshold.right_bound is Bound.INCLUSIVE:
                    meets_upper = corr <= cur_threshold.right_value
                elif cur_threshold.right_bound is Bound.EXCLUSIVE:
                    meets_upper = corr < cur_threshold.right_value

                edge_matches.append(meets_lower and meets_upper)

            # Depending on the filtering type, check if we should keep the edge
            if params.thresh_matching is BooleanAllAny.ALL:
                if all(edge_matches):
                    edges_to_keep.append((edge_from, edge_to))
            elif params.thresh_matching is BooleanAllAny.ANY:
                if any(edge_matches):
                    edges_to_keep.append((edge_from, edge_to))

        # Create a subgraph based on those edges that meet the filtering
        edge_subgraph = G.edge_subgraph(edges_to_keep)

        # Filter the nodes based on the degree
        nodes_to_keep = set()
        for cur_node, cur_degree in edge_subgraph.degree():
            if params.degree.min_value <= cur_degree <= params.degree.max_value:
                # Add the node and its neighbors to the list of nodes to keep
                nodes_to_keep.add(cur_node)
                nodes_to_keep.update(set(edge_subgraph.neighbors(cur_node)))

        # Create the subgraph containing only those nodes that meet the criteria
        composed = edge_subgraph.subgraph(nodes_to_keep)

        # If the user selected any nodes of interest, make sure they are included
        # in the final graph just as a node. If they aren't included by this point
        # then none of the metrics will be satisifed, so a node works.
        nodes_of_interest_missing = set()
        for cur_node_of_interest in params.node_of_interest:
            if not composed.has_node(cur_node_of_interest):
                nodes_of_interest_missing.add(cur_node_of_interest)
        # If any were found, unfreeze the graph and add them
        if len(nodes_of_interest_missing) > 0:
            composed = nx.Graph(composed)
            composed.add_nodes_from(nodes_of_interest_missing)
        composed = nx.Graph(composed)

        # Store the result in the cache
        to_pickle(composed, cache_path)

        # Return the filtered graph
        return composed

    def filter_to_cytoscape(self, params: NetworkFormStoreModel):
        filtered_graph = self.filter(params)

        # Convert the graph to cytoscape format
        cyto_data = nx.cytoscape_data(filtered_graph)
        out_graph = cyto_data['elements']

        # There is a formatting quirk with cytoscape that requires a reformat
        # to display the label correctly
        for node in out_graph['nodes']:
            node['data']['label'] = node['data']['name']
            del node['data']['name']

        # Add an identifier to each edge composed from the source/target
        for edge in out_graph['edges']:
            source = edge['data']['source']
            target = edge['data']['target']
            edge_id = sorted([f'{source}-{target}', f'{target}-{source}'])[0]
            edge['data']['id'] = edge_id

        return out_graph


class DistanceMatrixGraphStore(dcc.Store):
    """
    This class is used to represent the store for the distance matrix graph.
    """
    ID = 'distance-matrix-graph-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=dict()
        )
