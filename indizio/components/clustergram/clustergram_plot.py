from functools import lru_cache
from typing import Optional

import dash_bio
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, callback, State, dcc
from plotly.subplots import make_subplots

from indizio.config import GRAPH_AXIS_FONT_SIZE
from indizio.models.common.boolean import BooleanYesNo
from indizio.models.common.sync_with_network import SyncWithNetwork
from indizio.store.clustergram.parameters import ClustergramParametersStore, ClustergramParametersStoreModel
from indizio.store.metadata_file import MetadataFileStore, MetadataFileStoreModel
from indizio.store.network.interaction import NetworkInteractionStore, NetworkInteractionStoreModel
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceStoreModel
from indizio.store.tree_file import TreeFileStore, TreeFileStoreModel
from indizio.util.cache import freezeargs
from indizio.util.data import is_numeric
from indizio.util.graph import format_axis_labels
from indizio.util.log import log_debug
from indizio.util.trees import create_dendrogram_plot


class ClustergramPlot(dcc.Loading):
    """
    This component is the main clustergram plot.
    """

    ID = 'clustergram-plot'
    ID_GRAPH = f'{ID}-graph'
    ID_LOADING = f'{ID}-loading'

    def __init__(self):
        super().__init__(
            id=self.ID_LOADING,
            children=[
                dcc.Graph(
                    id=self.ID_GRAPH,
                    style={
                        'width': '100%',
                        'height': 'calc(100vh - 170px)'
                    },
                    responsive=True,
                )
            ]
        )

        @callback(
            output=dict(
                fig=Output(self.ID_GRAPH, "figure"),
            ),
            inputs=dict(
                ts_params=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                ts_dm=Input(PresenceAbsenceStore.ID, "modified_timestamp"),
                ts_tree=Input(TreeFileStore.ID, "modified_timestamp"),
                ts_meta=Input(MetadataFileStore.ID, "modified_timestamp"),
                ts_interaction=Input(NetworkInteractionStore.ID, "modified_timestamp"),
                state_params=State(ClustergramParametersStore.ID, "data"),
                state_dm=State(PresenceAbsenceStore.ID, "data"),
                state_tree=State(TreeFileStore.ID, "data"),
                state_meta=State(MetadataFileStore.ID, "data"),
                state_interaction=State(NetworkInteractionStore.ID, "data")
            )
        )
        @freezeargs
        @lru_cache
        def update_options_on_file_upload(
                ts_params, ts_dm, ts_tree, ts_meta, ts_interaction, state_params, state_dm,
                state_tree, state_meta, state_interaction
        ):
            log_debug(f'{self.ID_GRAPH} - Updating clustergram figure.')

            # De-serialize the distance matrix store
            state_dm = PresenceAbsenceStoreModel(**state_dm)
            params = ClustergramParametersStoreModel(**state_params)
            state_tree = TreeFileStoreModel(**state_tree)
            state_meta = MetadataFileStoreModel(**state_meta)
            state_interaction = NetworkInteractionStoreModel(**state_interaction)

            # Load the distance matrix based on what was used to generate the graph

            # Optionally load the metadata
            if params.metadata is not None:
                df_meta = state_meta.get_file(params.metadata).read()
            else:
                df_meta = None

            # Optionally load the tree
            if params.tree is not None and params.cluster_on.is_identifiers():
                tree = state_tree.get_file(params.tree).read()
            else:
                tree = None

            # If the metric is not set from the parameters, choose the first one
            if params.metric is None:
                feature_df = state_dm.get_files()[0].read()
            else:
                feature_df = state_dm.get_file(params.metric).read()

            # Subset the data visible if requested
            if params.sync_with_network is SyncWithNetwork.VISIBLE and len(state_interaction.nodes_visible) > 0:
                subset_cols = [x for x in feature_df.columns if x in state_interaction.nodes_visible]
                feature_df = feature_df[subset_cols]
            elif params.sync_with_network is SyncWithNetwork.SELECTED and len(state_interaction.nodes_selected) > 0:
                subset_cols = [x for x in feature_df.columns if x in state_interaction.nodes_selected]
                feature_df = feature_df[subset_cols]

            # To prevent an error on only one column visible, do not cluster
            if len(feature_df.columns) < 2:
                cluster_features = False
            else:
                cluster_features = params.cluster_on.is_features()

            # Generate the Clustergram using DashBio and return the traces
            feature_df, cg_traces, dendro_traces = generate_clustergram(
                feature_df=feature_df,
                tree=tree,
                optimal_leaf_ordering=params.optimal_leaf_order is BooleanYesNo.YES,
                cluster_features=cluster_features,
                cluster_ids=params.cluster_on.is_identifiers(),
            )

            # Using the DashBio data, create our own Clustergram figure
            # as the DashBio doesn't allow for multiple colour grouping (meta)
            fig = generate_annotation_heatmap(feature_df, cg_traces, df_meta, params, dendro_traces)

            fig.update_xaxes(tickangle=45, tickfont=dict(size=GRAPH_AXIS_FONT_SIZE))
            fig.update_yaxes(tickfont=dict(size=GRAPH_AXIS_FONT_SIZE))

            return dict(
                fig=fig,
            )


def generate_clustergram(
        feature_df: pd.DataFrame,
        tree: Optional[TreeFileStoreModel],
        optimal_leaf_ordering: bool,
        cluster_features: bool,
        cluster_ids: bool
):
    """
    Helper function to generate the clustergram and return the traces.
    """

    # Determine what type of clustering based on the input argument
    # Note this is a bit of legacy code left over from the original implementation
    # Later on in the program, the dendrogram will be displayed if requested
    if cluster_features and cluster_ids:
        cluster_arg = 'col'
    elif cluster_features:
        cluster_arg = 'col'
    elif cluster_ids:
        cluster_arg = None
    else:
        cluster_arg = None

    # If a tree has been provided then subset both the matrix and tree
    # to only those present in both and compute the distance matrix
    tree_taxa_ordered = None
    if tree is not None and cluster_ids:
        # Get the order of the leaf nodes (postorder)
        tree_taxa_ordered = [x.taxon.label for x in tree.leaf_node_iter()]

        # Subset feature dataframe to only those those present in the tree
        common_taxa = set(tree_taxa_ordered).intersection(set(feature_df.index))
        common_taxa = [x for x in feature_df.index if x in common_taxa]
        tree = tree.extract_tree_with_taxa_labels(common_taxa)
        feature_df = feature_df.filter(items=common_taxa, axis=0)

        # Order the Y axis values of the feature dataframe to match the tree
        tree_taxa_ordered = [x.taxon.label for x in tree.leaf_node_iter()]
        feature_df = feature_df.loc[tree_taxa_ordered]

    # Compute the clustergram
    clustergram, traces = dash_bio.Clustergram(
        data=feature_df.values,
        row_labels=feature_df.index.to_list(),
        column_labels=feature_df.columns.to_list(),
        optimal_leaf_order=optimal_leaf_ordering,
        link_fun=None,
        # dist_fun=dist_fun,
        # row_dist='euclidean', #  if not tree else 'row_dist'
        # col_dist='euclidean',
        cluster=cluster_arg,
        # hidden_labels='row',
        # height=900,
        # width=1100,
        color_map=[
            [0.0, '#FFFFFF'],
            [1.0, '#EF553B']
        ],
        return_computed_traces=True,
        line_width=2.0,
    )

    # Now that we have the positional information from the clustergram,
    # we generate the dendrogram (if requested)
    dendro_traces = list()
    if cluster_ids and tree:
        cluster_y_pos = traces['heatmap']['y']
        dendro_traces = create_dendrogram_plot(tree, cluster_y_pos, tree_taxa_ordered)

    return feature_df, traces, dendro_traces


def generate_annotation_heatmap(feature_df: pd.DataFrame, cg_traces, df_meta: Optional[MetadataFileStoreModel],
                                params: ClustergramParametersStoreModel, dendro_traces):
    """
    Creates the main clustergram figure
    """
    has_metadata = df_meta is not None and params.metadata is not None and len(params.metadata_cols) > 0
    n_meta_cols = len(params.metadata_cols) if has_metadata else 0

    # As the ordering of indices may have changed in the main heatmap, get the
    # names of the rows and columns in the correct order
    idx_to_row_label = [feature_df.index[x] for x in cg_traces['row_ids']]
    idx_to_col_label = [feature_df.columns[x] for x in cg_traces['column_ids']]

    # Set the dimensions/identifiers for the plot (variable columns)
    row_meta_left = 2
    row_dend_left, col_dend_left = 2, 1
    row_dend_top, col_dend_top = 1, 2 + n_meta_cols
    row_heat_main, col_heat_main = 2, 2 + n_meta_cols

    # The remaining space will be used by the metadata columns (if present)
    col_left_dendro_width = 20
    col_main_heatmap_width = 70 if n_meta_cols > 0 else 80
    if n_meta_cols > 0:
        col_meta_each = (100 - (col_main_heatmap_width + col_left_dendro_width)) / n_meta_cols
        column_widths = [col_left_dendro_width]
        [column_widths.append(col_meta_each) for _ in range(n_meta_cols)]
        column_widths.append(col_main_heatmap_width)
    else:
        column_widths = [col_left_dendro_width, col_main_heatmap_width]

    """
    Create subplots equal to the following:
        [empty]      [empty * params.metadata_cols]      [dendro_col] 
        [dendro_row] [meta_row * params.metadata_cols]   [heatmap]   
    """
    fig = make_subplots(
        rows=2,
        cols=2 + n_meta_cols,
        vertical_spacing=0,
        horizontal_spacing=0,
        shared_xaxes=True,
        shared_yaxes=True,
        column_widths=column_widths,
        row_heights=[20, 80],
    )

    """
    Create the main heatmap
    """
    # Create the hovertext for the heatmap
    xy_labels_full = list()
    for y in idx_to_row_label:
        cur_vals = list()
        for x in idx_to_col_label:
            cur_vals.append((y, x))
        xy_labels_full.append(cur_vals)

    main_heatmap = go.Heatmap(
        x=cg_traces['heatmap'].x,
        y=cg_traces['heatmap'].y,
        z=cg_traces['heatmap'].z,
        colorscale=((0.0, 'rgba(0,0,0,0)'), (1.0, '#EF553B')),
        showscale=False,
        xgap=1,
        ygap=1,
        customdata=np.array(xy_labels_full),
        hovertemplate='<b>ID:</b> %{customdata[0]}<br><b>Feature:</b> %{customdata[1]}',
        name='',
    )

    fig.add_trace(main_heatmap, row=row_heat_main, col=col_heat_main)

    # Add the tick labls
    fig.update_xaxes(
        ticktext=format_axis_labels(idx_to_col_label),
        tickvals=main_heatmap.x,
        row=row_heat_main,
        col=col_heat_main
    )
    fig.update_yaxes(
        ticktext=format_axis_labels(idx_to_row_label),
        tickvals=main_heatmap.y,
        row=row_heat_main,
        col=col_heat_main
    )

    """
    Create the dendrograms
    """
    if dendro_traces is not None:
        for dendro_trace in dendro_traces:
            fig.add_trace(dendro_trace, row=row_dend_left, col=col_dend_left)
    # for trace in cg_traces['dendro_traces']['row']:
    #     dendro_row = go.Scatter(trace, hoverinfo='skip')
    #     fig.add_trace(dendro_row, row=row_dend_left, col=col_dend_left)

    for trace in cg_traces['dendro_traces']['col']:
        dendro_col = go.Scatter(trace, hoverinfo='skip')
        fig.add_trace(dendro_col, row=row_dend_top, col=col_dend_top)

    """
    Add the metadata grouping
    """
    if has_metadata:
        for meta_col_idx, meta_col_value in enumerate(params.metadata_cols):
            meta_col_idx += 2

            left_meta, left_meta_y_ticks = generate_metadata_heatmap(
                feature_df,
                cg_traces,
                main_heatmap,
                df_meta,
                meta_col_value
            )
            fig.add_trace(left_meta, row=row_meta_left, col=meta_col_idx)
            fig.update_xaxes(
                ticktext=[meta_col_value], tickvals=left_meta.x,
                row=row_meta_left, col=meta_col_idx, tickangle=-60
            )
            fig.update_yaxes(
                ticktext=left_meta_y_ticks, tickvals=left_meta.y,
                row=row_meta_left, col=meta_col_idx
            )

    """
    Styling
    """

    # Hide the legend
    fig.update_layout(showlegend=False)

    # Make the background transparent
    fig.update_layout({
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
    })

    # Hide the axis labels for all subplots
    fig.update_xaxes(showticklabels=False, showgrid=False, zerolinecolor='rgba(0,0,0,0)')
    fig.update_yaxes(showticklabels=False, showgrid=False, zerolinecolor='rgba(0,0,0,0)')

    # Show axis labels for select subplots
    fig.update_xaxes(showticklabels=True, row=row_heat_main, col=col_heat_main)
    fig.update_yaxes(showticklabels=True, row=row_heat_main, col=col_heat_main)

    # Change the location of the axes for select subplots
    fig.update_yaxes(side="right", row=row_heat_main, col=col_heat_main)

    # Update the metadata axes
    for meta_col_idx in range(n_meta_cols):
        meta_col_idx += 2

        # Show axis labels for select subplots
        fig.update_xaxes(showticklabels=True, row=row_meta_left, col=meta_col_idx)

        # Prevent zooming for certain axes
        fig.update_xaxes(fixedrange=True, row=row_meta_left, col=meta_col_idx)

    return fig


def generate_metadata_heatmap(
        feature_df: pd.DataFrame,
        cg_traces,
        main_heatmap,
        df_meta: pd.DataFrame,
        column_name: str
):
    # Create the data matrix
    heat_data = np.zeros((feature_df.shape[0], 1), dtype=float)
    heat_text = np.zeros(heat_data.shape, dtype=object)

    # Extract the values for this column
    cur_col = df_meta[column_name]

    # Check if this is a numerical or categorical column
    all_numeric = all(is_numeric(x, nan_not_numeric=False) for x in cur_col.values)

    # If this is a numeric column, assign a color gradient to the values
    if not all_numeric:
        d_value_to_idx = {k: i for i, k in enumerate(cur_col.values)}

        # Iterate over each value in the current column to assign a value
        for row_idx, cur_value in enumerate(cur_col.values):
            heat_data[row_idx, 0] = d_value_to_idx[cur_value]
            heat_text[row_idx, 0] = cur_value

    else:
        # Iterate over each value in the current column to assign a value
        for row_idx, cur_value in enumerate(cur_col.values):
            heat_data[row_idx, 0] = cur_value
            heat_text[row_idx, 0] = cur_value

    # Re-order the heatmap to be consistent with the main heatmap clustering
    heat_data = heat_data[cg_traces['row_ids'], :]
    heat_text = heat_text[cg_traces['row_ids'], :]

    # Create the heatmap and return it
    left_meta = go.Heatmap(
        x=list(range(heat_data.shape[1])),
        y=main_heatmap.y,
        z=heat_data,
        colorscale='agsunset',
        showscale=False,
        name='',
        customdata=heat_text,
        hovertemplate='<b>ID:</b> %{y}<br><b>%{x}</b>: %{customdata}'
    )

    row_names = [feature_df.index[x] for x in cg_traces['row_ids']]
    return left_meta, row_names
