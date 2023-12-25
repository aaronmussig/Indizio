from collections import defaultdict
from pathlib import Path
from typing import List, Optional, Collection, FrozenSet

import networkx as nx
from dash import dcc
from diskcache import Cache
from pydantic import BaseModel

from indizio.cache import CACHE
from indizio.config import PERSISTENCE_TYPE, ENABLE_CACHE
from indizio.interfaces.boolean import BooleanAllAny, BooleanShowHide
from indizio.interfaces.bound import Bound
from indizio.store.distance_matrix import DistanceMatrixFile
from indizio.store.network_form_store import NetworkFormStoreData
from indizio.util.dataframe import dataframe_to_pairs
from indizio.util.files import to_pickle, from_pickle
from indizio.util.graph import neighborhood
from indizio.util.hashing import calc_md5
from indizio.util.types import ProgressFn


class DmGraph(BaseModel):
    path: Path
    matrices: List[DistanceMatrixFile]
    hash: str

    @classmethod
    def from_distance_matricies(
            cls,
            matrices: Collection[DistanceMatrixFile],
            set_progress: Optional[ProgressFn] = None
    ):
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

    def get_metrics(self) -> FrozenSet[str]:
        """Return all metrics used in the construction of the graph edges."""
        out = set()
        for dm in self.matrices:
            out.add(dm.file_id)
        return frozenset(out)

    def filter_to_cytoscape(self, params: NetworkFormStoreData):

        if ENABLE_CACHE:
            # Extract the caching key from the parameters
            param_cache_key = params.get_cache_key()
            combined_cache_key = calc_md5(self.hash.encode() + param_cache_key)
            cache_key = f'cyto-graph-{combined_cache_key}'

            # Check if the graph is already cached
            with Cache(CACHE.directory) as cache:
                existing_result = cache.get(cache_key)
                if existing_result:
                    print("returning from cache")
                    return existing_result

        # No existing data were found, compute it
        print('reading graph')
        G = self.read()
        print('read')

        # Extract all edges for procesing
        # Filter the nodes if specified
        nodes_to_keep = params.node_of_interest if params.node_of_interest else list(G.nodes)
        edges_to_process = G.edges(nodes_to_keep, data=True)

        # Iterate over each edge and filter them based on the thresholding
        edges_to_keep = list()
        print('calculating from edges')
        for edge_from, edge_to, d_edge_data in edges_to_process:

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
                    edges_to_keep.append((edge_from,edge_to))


        # Create a subgraph based on those edges that meet the filtering
        print("create subgraph")
        edge_subgraph = G.edge_subgraph(edges_to_keep)

        # Filter the nodes based on the degree
        print('filter nodes to keep')
        nodes_to_keep = set()
        for cur_node, cur_degree in edge_subgraph.degree():
            if params.degree.min_value <= cur_degree <= params.degree.max_value:
                # Add the node and its neighbors to the list of nodes to keep
                nodes_to_keep.add(cur_node)
                nodes_to_keep.update(set(edge_subgraph.neighbors(cur_node)))

        # Create the subgraph containing only those nodes that meet the criteria
        print("composing")
        composed = edge_subgraph.subgraph(nodes_to_keep)
        print("done")

        # print()
        # subgraphs = list()
        #
        # nodes_to_keep = params.node_of_interest if params.node_of_interest else list(G.nodes)
        # print("finding nodes to keep")
        # # For each node, iterate over each edge that connects to it
        # for i, node in enumerate(nodes_to_keep):
        #     edges = list()
        #     for edge in G.edges(node, data=True):
        #
        #         # Check each of the edge attributes to see if it is within bounds
        #         file_matches = list()
        #         for file_id, corr in edge[2].items():
        #             cur_threshold = params.thresholds[file_id]
        #
        #             meets_lower = False
        #             if cur_threshold.left_bound is Bound.INCLUSIVE:
        #                 meets_lower = corr >= cur_threshold.left_value
        #             elif cur_threshold.left_bound is Bound.EXCLUSIVE:
        #                 meets_lower = corr > cur_threshold.left_value
        #
        #             meets_upper = False
        #             if cur_threshold.right_bound is Bound.INCLUSIVE:
        #                 meets_upper = corr <= cur_threshold.right_value
        #             elif cur_threshold.right_bound is Bound.EXCLUSIVE:
        #                 meets_upper = corr < cur_threshold.right_value
        #
        #             file_matches.append(meets_lower and meets_upper)
        #
        #         # Depending on the filtering type, check if we should keep the edge
        #         if params.thresh_matching is BooleanAllAny.ALL:
        #             if all(file_matches):
        #                 edges.append((edge[0], edge[1]))
        #         elif params.thresh_matching is BooleanAllAny.ANY:
        #             if any(file_matches):
        #                 edges.append((edge[0], edge[1]))
        #
        #     # Subset the original graph to contain only these edges
        #     H = G.edge_subgraph(edges)
        #     for node_id, node_degree in H.degree():
        #         if params.degree.min_value <= node_degree <= params.degree.max_value:
        #             continue
        #     if node in set(H.nodes):
        #         if params.thresh_degree == 0:
        #             subgraphs.append(H)
        #         else:
        #             subgraphs.append(H.subgraph(neighborhood(H, node, params.thresh_degree)))
        #     else:
        #         subgraphs.append(G.subgraph([node]))
        #
        #     # Update the progress function if provided
        #     # if progress:
        #     #     progress(100 * i / len(nodes_to_keep))
        # print('composing')
        # composed = nx.compose_all(subgraphs)


        # Convert the graph to cytoscape format
        print('converitng to cytoscape')
        cyto_data = nx.cytoscape_data(composed)
        out_graph = cyto_data['elements']

        # There is a formatting quirk with cytoscape that requires a reformat
        # to display the label correctly
        for node in out_graph['nodes']:
            node['data']['label'] = node['data']['name']
            del node['data']['name']

        # Store the result in the cache
        if ENABLE_CACHE:
            print('saving in cache')
            with Cache(CACHE.directory) as cache:
                cache.set(cache_key, out_graph)
        return out_graph


class DistanceMatrixGraphStore(dcc.Store):
    ID = 'distance-matrix-graph-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
