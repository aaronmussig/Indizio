import logging
from typing import Optional

import dash_bio
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Output, Input, callback, State, dcc
from dash.exceptions import PreventUpdate
from phylodm import PhyloDM
from plotly.subplots import make_subplots
from scipy.spatial.distance import squareform, pdist

from indizio.interfaces.boolean import BooleanYesNo
from indizio.store.clustergram_parameters import ClustergramParametersStore, ClustergramParameters
from indizio.store.metadata_file import MetadataFileStore, MetadataData
from indizio.store.presence_absence import PresenceAbsenceStore, PresenceAbsenceData
from indizio.store.tree_file import TreeFileStore, TreeData


class ClustergramPlot(dcc.Graph):
    ID = 'clustergram-plot'

    def __init__(self):
        super().__init__(
            id=self.ID,
            style={
                'width': 'min(calc(100vh - 170px), 100vw)',
                'height': 'min(calc(100vh - 170px), 100vw)'
            },
            responsive=True,
        )

        @callback(
            output=dict(
                fig=Output(self.ID, "figure"),
            ),
            inputs=dict(
                ts_params=Input(ClustergramParametersStore.ID, "modified_timestamp"),
                ts_dm=Input(PresenceAbsenceStore.ID, "modified_timestamp"),
                ts_tree=Input(TreeFileStore.ID, "modified_timestamp"),
                ts_meta=Input(MetadataFileStore.ID, "modified_timestamp"),
                state_params=State(ClustergramParametersStore.ID, "data"),
                state_dm=State(PresenceAbsenceStore.ID, "data"),
                state_tree=State(TreeFileStore.ID, "data"),
                state_meta=State(MetadataFileStore.ID, "data"),
            )
        )
        # @freezeargs
        # @lru_cache
        def update_options_on_file_upload(ts_params, ts_dm, ts_tree, ts_meta, state_params, state_dm, state_tree,
                                          state_meta):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating clustergram figure.')

            if ts_dm is None or not state_dm:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialize the distance matrix store
            state_dm = PresenceAbsenceData(**state_dm)
            params = ClustergramParameters(**state_params)
            state_tree = TreeData(**state_tree)
            state_meta = MetadataData(**state_meta)

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

            # Generate the Clustergram using DashBio and return the traces
            feature_df, cg_traces = generate_clustergram(
                feature_df=feature_df,
                tree=tree,
                optimal_leaf_ordering=params.optimal_leaf_order is BooleanYesNo.YES,
                cluster_features=params.cluster_on.is_features(),
                cluster_ids=params.cluster_on.is_identifiers(),
            )

            # Using the DashBio data, create our own Clustergram figure
            # as the DashBio doesn't allow for multiple colour grouping (meta)
            print('creating fig')
            fig = generate_annotation_heatmap(feature_df, cg_traces, df_meta)

            # Disable the heatmap levend as only boolean values are shown
            # for cur_item in clustergram.data:
            #     if isinstance(cur_item, go.Heatmap):
            #         cur_item.showscale = False

            # clustergram.update_layout(
            #     yaxis_scaleanchor="x"
            # )

            return dict(
                fig=fig,

            )


def generate_clustergram(
        feature_df: pd.DataFrame,
        tree: Optional[TreeData],
        optimal_leaf_ordering: bool,
        cluster_features: bool,
        cluster_ids: bool
):
    """
    Helper function to generate the clustergram and return the traces.
    """

    # Determine what type of clustering based on the input argument
    if cluster_features and cluster_ids:
        cluster_arg = 'all'
    elif cluster_features:
        cluster_arg = 'col'
    elif cluster_ids:
        cluster_arg = 'row'
    else:
        cluster_arg = None

    # If a tree has been provided then subset both the matrix and tree
    # to only those present in both and compute the distance matrix
    if tree is not None and cluster_ids:
        common_taxa = {x.label for x in tree.taxon_namespace}.intersection(set(feature_df.index))
        common_taxa = [x for x in feature_df.index if x in common_taxa]
        tree = tree.extract_tree_with_taxa_labels(common_taxa)
        feature_df = feature_df.filter(items=common_taxa, axis=0)

        # Convert the tree to a linkage object
        tree_pdm = PhyloDM.load_from_dendropy(tree)
        tree_pdm.compute_row_vec()

        # Sort the PDM in the same order as given in the feature matrix
        tree_dm = np.zeros((len(common_taxa), len(common_taxa)))
        for i, taxon_i in enumerate(feature_df.index):
            for j, taxon_j in enumerate(feature_df.index):
                tree_dm[i, j] = tree_pdm.distance(taxon_i, taxon_j)

        tree_dm_square = squareform(tree_dm)

        def dist_fun(X, metric='euclidean', *, out=None, **kwargs):
            # Check if the tree was provided, and if so, compute the distance using it
            if metric == 'row_dist':
                return tree_dm_square
            # Column distances will always be computed without any additional tree info
            else:
                return pdist(X, metric='euclidean', out=out, **kwargs)

    else:
        dist_fun = pdist

    print('creating CG')
    clustergram, traces = dash_bio.Clustergram(
        data=feature_df.values,
        row_labels=feature_df.index.to_list(),
        column_labels=feature_df.columns.to_list(),
        optimal_leaf_order=optimal_leaf_ordering,
        # link_fun=phylo_linkage,
        dist_fun=dist_fun,
        row_dist='euclidean' if not tree else 'row_dist',
        cluster=cluster_arg,
        # hidden_labels='row',
        # height=900,
        # width=1100,
        color_map=[
            [0.0, '#FFFFFF'],
            [1.0, '#EF553B']
        ],
        return_computed_traces=True,
    )
    return feature_df, traces


def generate_annotation_heatmap(feature_df: pd.DataFrame, cg_traces, df_meta: Optional[MetadataData]):
    """
    Creates the main clustergram figure
    """

    # As the ordering of indices may have changed in the main heatmap, get the
    # names of the rows and columns in the correct order
    idx_to_row_label = [feature_df.index[x] for x in cg_traces['row_ids']]
    idx_to_col_label = [feature_df.columns[x] for x in cg_traces['column_ids']]

    """
    Create subplots equal to the following:
        [empty]      [empty]      [dendro_col] 
        [dendro_row] [meta_row]   [heatmap]   
    """

    subplot_spacing = [25, 10, 80]
    fig = make_subplots(
        rows=2,
        cols=3,
        vertical_spacing=0,
        horizontal_spacing=0,
        shared_xaxes=True,
        shared_yaxes=True,
        column_widths=[20, 10, 70],
        row_heights=[20, 80],
    )

    row_meta_left, col_meta_left = 2, 2
    row_dend_left, col_dend_left = 2, 1

    row_dend_top, col_dend_top = 1, 3

    row_heat_main, col_heat_main = 2, 3

    # for trace in go.Figure(clustergram).data:
    #     fig.add_trace(trace, row=1, col=2)
    # fig.add_trace(test, row=1, col=1)

    # fig.update_layout(clustergram.layout)

    """
    Create the main heatmap
    """

    # Use the pre-computed matrix from the DashBio library
    main_heatmap = go.Heatmap(
        cg_traces['heatmap'],
        colorscale=((0.0, '#FFFFFF'), (1.0, '#EF553B')),
        showscale=False,
        hovertemplate='<b>ID:</b> %{y}<br><b>Feature:</b> %{x}',
        name=''
    )

    fig.add_trace(main_heatmap, row=row_heat_main, col=col_heat_main)

    # Remove the colorbar as it is not needed
    # trace_heatmap.update_layout(coloraxis_showscale=False)
    # main_heatmap.data[0].showscale = False

    # Add the tick labls
    fig.update_xaxes(
        ticktext=idx_to_col_label, tickvals=main_heatmap.x,
        row=row_heat_main, col=col_heat_main
    )
    fig.update_yaxes(
        ticktext=idx_to_row_label, tickvals=main_heatmap.y,
        row=row_heat_main, col=col_heat_main
    )

    """
    Create the dendrograms
    """
    for trace in cg_traces['dendro_traces']['row']:
        dendro_row = go.Scatter(trace, hoverinfo='skip')
        fig.add_trace(dendro_row, row=row_dend_left, col=col_dend_left)

    for trace in cg_traces['dendro_traces']['col']:
        dendro_col = go.Scatter(trace, hoverinfo='skip')
        fig.add_trace(dendro_col, row=row_dend_top, col=col_dend_top)

    """
    Add the metadata grouping
    """
    if df_meta is not None:
        left_meta, left_meta_x_ticks, left_meta_y_ticks = generate_metadata_heatmap(feature_df, cg_traces, main_heatmap,
                                                                                    df_meta)
        fig.add_trace(left_meta, row=row_meta_left, col=col_meta_left)
        fig.update_xaxes(
            ticktext=left_meta_x_ticks, tickvals=left_meta.x,
            row=row_meta_left, col=col_meta_left, tickangle=-90
        )
        fig.update_yaxes(
            ticktext=left_meta_y_ticks, tickvals=left_meta.y,
            row=row_meta_left, col=col_meta_left
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
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)

    # Show axis labels for select subplots
    fig.update_xaxes(showticklabels=True, row=row_meta_left, col=col_meta_left)
    fig.update_xaxes(showticklabels=True, row=row_heat_main, col=col_heat_main)
    fig.update_yaxes(showticklabels=True, row=row_heat_main, col=col_heat_main)

    # Change the location of the axes for select subplots
    fig.update_yaxes(side="right", row=row_heat_main, col=col_heat_main)

    # Prevent zooming for certain axes
    fig.update_xaxes(fixedrange=True, row=row_meta_left, col=col_meta_left)

    return fig


def generate_metadata_heatmap(feature_df: pd.DataFrame, cg_traces, main_heatmap, df_meta: pd.DataFrame):
    # Extract relevant information from the feature dataframe
    d_id_to_row_idx = {x: i for i, x in enumerate(feature_df.index)}

    # Assign a unique color index to each unique value in each column
    colors = px.colors.qualitative.Plotly
    cur_color = 1  # the first colour is reserved for nothing
    d_col_to_colors = dict()
    column_names = list()
    for col_idx, meta_col in enumerate(df_meta.columns):
        d_col_colors = dict()
        d_value_to_color = dict()
        for row_idx, meta_row in enumerate(df_meta.index):
            cur_value = df_meta.values[row_idx, col_idx]
            if cur_value not in d_value_to_color:
                d_value_to_color[cur_value] = cur_color
                cur_color += 1
            d_col_colors[meta_row] = d_value_to_color[cur_value]
        d_col_to_colors[meta_col] = d_col_colors
        column_names.append(meta_col)

    # Add any missing values to the color dictionary
    all_ids = frozenset(feature_df.index)
    for cur_col in d_col_to_colors:
        for cur_id in all_ids - set(d_col_to_colors[cur_col]):
            d_col_to_colors[cur_col][cur_id] = 0

    # Assign the Z value for each cell in the heatmap
    step = round(1 / cur_color, 10)
    heat_data = np.zeros((feature_df.shape[0], df_meta.shape[1]), dtype=float)
    heat_text = np.zeros(heat_data.shape, dtype=object)
    heat_text.fill('N/A')
    for col_idx, meta_col in enumerate(df_meta.columns):
        for meta_row in df_meta.index:
            row_idx = d_id_to_row_idx[meta_row]
            heat_data[row_idx, col_idx] = d_col_to_colors[meta_col][meta_row] * step
            heat_text[row_idx, col_idx] = df_meta.values[row_idx, col_idx]

    # Create the colorscale to contain discrete bins
    colorscale_new = list()
    for i in range(cur_color):
        if i == 0:
            cur_color_hex = '#FFFFFF'
        else:
            cur_color_hex = colors[i % len(colors)]
        colorscale_new.append([i * step, cur_color_hex])
        colorscale_new.append([(i + 1) * step, cur_color_hex])
    colorscale_new[-1][0] = 1.0

    # Re-order the heatmap to be consistent with the main heatmap clustering
    heat_data = heat_data[cg_traces['row_ids'], :]
    heat_text = heat_text[cg_traces['row_ids'], :]

    # Create the heatmap and return it
    left_meta = go.Heatmap(
        x=list(range(heat_data.shape[1])),
        y=main_heatmap.y,
        z=heat_data,
        colorscale=colorscale_new,
        showscale=False,
        name='',
        customdata=heat_text,
        hovertemplate='<b>ID:</b> %{y}<br><b>%{x}</b>: %{customdata}'
    )

    row_names = [feature_df.index[x] for x in cg_traces['row_ids']]
    return left_meta, column_names, row_names
