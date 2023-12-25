from typing import Optional

import networkx as nx

from indizio.store.network_form_store import NetworkThreshCorrOption
from indizio.util.types import ProgressFn


def filter_graph(
        G: nx.Graph,
        node_subset,
        degree,
        thresh,
        thresh_op: NetworkThreshCorrOption,
        progress: Optional[ProgressFn] = None
) -> nx.Graph:
    subgraphs = list()

    # Filter the nodes if specified
    nodes_to_keep = node_subset if node_subset else list(G.nodes)

    for i, node in enumerate(nodes_to_keep):
        edges = list()
        # TODO: Here I have removed the requirement for the degree to be 0
        # TODO: as it doesn't make any sense for filtering
        for edge in G.edges(node, data=True):
            for file_name, corr in edge[2].items():
                keep_edge = False
                if thresh_op is NetworkThreshCorrOption.GT:
                    if corr > thresh:
                        keep_edge = True
                elif thresh_op is NetworkThreshCorrOption.GEQ:
                    if corr >= thresh:
                        keep_edge = True
                elif thresh_op is NetworkThreshCorrOption.EQ:
                    if corr == thresh:
                        keep_edge = True
                elif thresh_op is NetworkThreshCorrOption.LEQ:
                    if corr <= thresh:
                        keep_edge = True
                elif thresh_op is NetworkThreshCorrOption.LT:
                    if corr < thresh:
                        keep_edge = True
                else:
                    raise ValueError(f'Unknown thresh_op: {thresh_op}')

                if keep_edge:
                    edges.append((edge[0], edge[1]))

        H = G.edge_subgraph(edges)
        if node in set(H.nodes):
            if degree == 0:
                subgraphs.append(H)
            else:
                subgraphs.append(H.subgraph(neighborhood(H, node, degree)))
        else:
            subgraphs.append(G.subgraph([node]))

        # Update the progress function if provided
        if progress:
            progress(100 * i / len(nodes_to_keep))
    composed = nx.compose_all(subgraphs)
    return composed


def neighborhood(G, node, n):
    path_lengths = nx.single_source_dijkstra_path_length(G, node, n)
    return list(path_lengths.keys())
