import logging

import dash_bio
import numpy as np
import plotly.graph_objects as go
from dash import Output, Input, callback, State, dcc
from dash.exceptions import PreventUpdate
from phylodm import PhyloDM
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform

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

            # If the metric is not set from the parameters, choose the first one
            if params.metric is None:
                feature_df = state_dm.get_files()[0].read()
            else:
                feature_df = state_dm.get_file(params.metric).read()

            # If a tree has been provided then subset both the matrix and tree
            # to only those present in both and compute the distance matrix
            if params.tree is not None:
                tree = state_tree.get_file(params.tree).read()
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
                tree_linkage = linkage(tree_dm_square)

                def phylo_linkage(y, method='single', metric='euclidean', optimal_ordering=False):
                    """
                    A hack to allow us to use Clustergram. Linkage is precomputed
                    """
                    return tree_linkage

            else:
                phylo_linkage = None

            clustergram = dash_bio.Clustergram(
                data=feature_df.values,
                row_labels=feature_df.index.to_list(),
                column_labels=feature_df.columns.to_list(),
                link_fun=phylo_linkage,
                cluster='row',
                hidden_labels='row',
                height=900,
                width=1100,
                color_map=[
                    [0.0, '#FFFFFF'],
                    [1.0, '#EF553B']
                ],
                return_computed_traces=True,
                # row_colors=['#FF00FF', '#00FF00', '#000000', '#EF553B', '#19D3F3'],
                # row_colors_label='Foobar'
            )
            clustergram, clst_traces = clustergram

            colors = ['#FF00FF', '#00FF00', '#000000', '#EF553B', '#19D3F3']
            colorscale = []




            # As the rows may have been re-ordered due to clustering, select
            # the correct color
            row_colorscale = list()
            for cur_idx, cur_coord in zip(clst_traces['row_ids'], clst_traces['heatmap'].y):
                row_colorscale.append(colors[cur_idx])


            i = 0

            step = round(1 / len(colors), 10)

            for color in colors:
                colorscale.append([i, color])
                i = round(i + step, 10)
                colorscale.append([i, color])

            colorscale[-1][0] = 1

            z = [[i] for i in range(len(colors))]

            test = go.Heatmap(
                x=[0],
                y=[5, 15, 25, 35, 45],
                z=z,
                colorscale=colorscale,
                colorbar={"xpad": 100},
                showscale=False,
                text=['test']
            )

            """
            Initialise the plot using the following layout
            [empty]      [empty]      [dendro_col]      [dendro_col]
            [empty]      [empty]      [meta_col]        [meta_col]
            [dendro_row] [meta_row]   [heatmap]         [heatmap]
            [dendro_row] [meta_row]   [heatmap]         [heatmap]
            """


            fig = make_subplots(
                rows=4,
                cols=4,
                specs=[
                    [{}, {}, {"colspan": 2}, None],
                    [{}, {}, {"colspan": 2}, None],
                    [{"rowspan": 2}, {"rowspan": 2}, {"colspan": 2, "rowspan": 2}, None],
                    [None, None, None, None],
                ],
                vertical_spacing=0,
                horizontal_spacing=0,
                print_grid=False,
                shared_xaxes=True,
                shared_yaxes=True,
            )

            # for trace in go.Figure(clustergram).data:
            #     fig.add_trace(trace, row=1, col=2)
            # fig.add_trace(test, row=1, col=1)

            # fig.update_layout(clustergram.layout)

            fig.add_trace(clst_traces['heatmap'], row=2, col=3)
            # fig.add_trace(clst_traces['dendro_traces']['row'], row=2, col=1)

            for trace in clst_traces['dendro_traces']['row']:
                dendro_row = go.Scatter(trace)
                fig.add_trace(dendro_row, row=2, col=1)

            for trace in clst_traces['dendro_traces']['col']:
                dendro_col = go.Scatter(trace)
                fig.add_trace(dendro_col, row=1, col=3)

            fig.add_trace(test, row=2, col=2)

            # Disable the heatmap levend as only boolean values are shown
            for cur_item in clustergram.data:
                if isinstance(cur_item, go.Heatmap):
                    cur_item.showscale = False

            # clustergram.update_layout(
            #     yaxis_scaleanchor="x"
            # )

            return dict(
                fig=fig,

            )



def generate_annotation_heatmap():
    return
