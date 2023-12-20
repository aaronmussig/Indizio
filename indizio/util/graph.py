import networkx as nx

from indizio.store.network_form_store import NetworkThreshCorrOption


def filter_graph(G: nx.Graph, node_subset, degree, thresh, thresh_op: NetworkThreshCorrOption):
    subgraphs = list()

    # Filter the nodes if specified
    nodes_to_keep = node_subset if node_subset else list(G.nodes)

    for node in nodes_to_keep:
        node_list = list()
        if degree == 0:
            node_list.append(node)
        edges = list()
        for edge in G.edges(node_list, data=True):
            for file_name in set(edge[2]) - {'target', 'source'}:
                keep_edge = False
                corr = edge[2][file_name]
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

    composed = nx.compose_all(subgraphs)
    return nx.cytoscape_data(composed)


def neighborhood(G, node, n):
    path_lengths = nx.single_source_dijkstra_path_length(G, node)
    return [node for node, length in path_lengths.items()
            if length <= n]
