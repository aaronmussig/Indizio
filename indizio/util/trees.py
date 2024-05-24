from collections import deque, defaultdict
from typing import Dict

import dendropy
import numpy as np
import plotly.graph_objects as go


def get_nodes_to_depth(tree: dendropy.Tree):
    out = defaultdict(list)
    queue = deque([(tree.seed_node, 0)])
    while len(queue) > 0:
        cur_node, cur_depth = queue.pop()
        out[cur_depth].append(cur_node)
        for child_node in cur_node.child_node_iter():
            queue.append((child_node, cur_depth + 1))
    return dict(out)


def get_leaf_parent_binary(tree: dendropy.Tree):
    """Returns all leaf node parents that have two leaf children."""
    d_parent_to_seen = defaultdict(lambda: 0)
    for leaf_node in tree.leaf_iter():
        d_parent_to_seen[leaf_node.parent_node] += 1
    out = list()
    for node, n_seen in d_parent_to_seen.items():
        if n_seen > 1:
            out.append(node)
    return out


def convert_dendropy_tree_to_linkage_matrix(tree: dendropy.Tree, order: list) -> np.array:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html

    # Compute the output dataset
    last_cluster_id = (len(order) - 1) * 2
    d_out_tmp = dict()

    # Traverse down the tree and assign a cluster ID to each group
    queue = deque([(tree.seed_node, last_cluster_id)])
    while len(queue) > 0:
        cur_node, cur_cluster_id = queue.popleft()

        # Stop processing if we have reached the tips of the tree
        if cur_node.is_leaf():
            break

        left_child, right_child = cur_node.child_nodes()

        if left_child.is_leaf():
            left_idx = order.index(left_child.taxon.label)
        else:
            left_idx = last_cluster_id - 1
            last_cluster_id = left_idx
            queue.append((left_child, left_idx))

        if right_child.is_leaf():
            right_idx = order.index(right_child.taxon.label)
        else:
            right_idx = last_cluster_id - 1
            last_cluster_id = right_idx
            queue.append((right_child, right_idx))

        cur_dist = left_child.edge_length + right_child.edge_length

        # The final item is the number of children but as far as I can
        # tell this isn't used
        d_out_tmp[cur_cluster_id] = (left_idx, right_idx, cur_dist, 1)

    # Consider the distance between the points as the X axis in the plot.
    # i.e. it is how high the node is from the cladograms base.

    # Reformat the dictionary to an array
    out = list()
    for _, row in sorted(d_out_tmp.items(), key=lambda x: x[0]):
        out.append(row)
    out = np.array(out)

    # The cluster distances need to be monotonic increasing, assign their
    # cluster id instead

    out[0, 2] = 1
    out[1, 2] = 2
    out[2, 2] = 3
    out[3, 2] = 4
    out[4, 2] = 5
    out[5, 2] = 60

    return out


def get_leaf_to_root(tree: dendropy.Tree) -> Dict[dendropy.Node, float]:
    out = dict()
    queue = deque([(tree.seed_node, 0)])
    while len(queue) > 0:
        cur_node, cur_dist = queue.pop()
        for child_node in cur_node.child_node_iter():
            queue.append((child_node, cur_dist + child_node.edge_length))
        if cur_node.is_leaf():
            out[cur_node] = cur_dist
    return out


def create_dendrogram_plot(tree, y_pos, tree_taxa_ordered):
    d_taxon_to_y = {t: y for t, y in zip(tree_taxa_ordered, y_pos)}

    trace_style = {
        'hoverinfo': 'skip',
        'mode': 'lines',
        'line': go.scatter.Line(color="#0074d9")
    }
    traces = list()

    # Determine the distance to the root for each node, this will be used
    # to pad the x axis
    leaf_to_root = get_leaf_to_root(tree)
    node_coords = dict()

    # Get the depth of each node, need to work up from that
    d_depth_to_nodes = get_nodes_to_depth(tree)

    for cur_depth, nodes_at_depth in sorted(d_depth_to_nodes.items(), key=lambda x: -x[0]):

        # Do not process the seed node
        if cur_depth == 0:
            break

        for cur_node in nodes_at_depth:

            # If this is a leaf node, then create the line
            if cur_node.is_leaf():
                cur_taxon = cur_node.taxon.label
                leaf_dist = leaf_to_root[cur_node]
                leaf_y = d_taxon_to_y[cur_taxon]
                x0 = leaf_dist - cur_node.edge_length
                traces.append(go.Scatter(x=[x0, leaf_dist], y=[leaf_y, leaf_y], **trace_style))
                node_coords[cur_node] = (x0, leaf_y)

            # Otherwise, create the clade connection
            else:

                # Get the coordinates from the children
                cur_children = cur_node.child_nodes()
                cur_children_coords = [node_coords[x] for x in cur_children]

                # Get the coordinates
                x_coord = cur_children_coords[0][0]
                top_y_coord = max(x[1] for x in cur_children_coords)
                bot_y_coord = min(x[1] for x in cur_children_coords)

                # Create the vertical line
                traces.append(go.Scatter(x=[x_coord, x_coord], y=[top_y_coord, bot_y_coord], **trace_style))

                # Create the horizontal line
                horizontal_y = (top_y_coord + bot_y_coord) / 2
                x0 = x_coord - cur_node.edge_length
                traces.append(go.Scatter(x=[x0, x_coord], y=[horizontal_y, horizontal_y], **trace_style))

                node_coords[cur_node] = (x0, horizontal_y)

    # Vertical connect from the seed node
    seed_children = tree.seed_node.child_nodes()
    seed_children_coords = [node_coords[x] for x in seed_children]
    x_coord = seed_children_coords[0][0]
    top_y_coord = max(x[1] for x in seed_children_coords)
    bot_y_coord = min(x[1] for x in seed_children_coords)
    traces.append(go.Scatter(x=[x_coord, x_coord], y=[top_y_coord, bot_y_coord], **trace_style))

    return traces
