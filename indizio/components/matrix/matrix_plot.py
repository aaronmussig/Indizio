import time
from functools import lru_cache

import numpy as np
import plotly.graph_objects as go
from dash import Output, Input, callback, State, dcc
from dash.exceptions import PreventUpdate

from indizio.config import GRAPH_AXIS_FONT_SIZE
from indizio.models.common.sync_with_network import SyncWithNetwork
from indizio.store.matrix.dm_files import DistanceMatrixStore, DistanceMatrixStoreModel
from indizio.store.matrix.parameters import MatrixParametersStore, MatrixParametersStoreModel
from indizio.store.network.interaction import NetworkInteractionStore, NetworkInteractionStoreModel
from indizio.util.cache import freezeargs
from indizio.util.graph import format_axis_labels
from indizio.util.log import log_debug, pretty_fmt_seconds
from indizio.util.plot import get_color


class MatrixPlot(dcc.Loading):
    """
    This contains the heatmap used in the matrix plot.
    """

    ID = 'matrix-plot'
    ID_LOADING = 'matrix-plot-loading'

    def __init__(self):
        super().__init__(
            id=self.ID_LOADING,
            children=[
                dcc.Graph(
                    id=self.ID,
                    style={
                        'width': 'min(calc(100vh - 150px), 100vw)',
                        'height': 'min(calc(100vh - 150px), 100vw)'
                    },
                    responsive=True,
                )
            ]
        )

        @callback(
            output=dict(
                fig=Output(self.ID, "figure"),
            ),
            inputs=dict(
                ts_params=Input(MatrixParametersStore.ID, "modified_timestamp"),
                ts_dm=Input(DistanceMatrixStore.ID, "modified_timestamp"),
                ts_interaction=Input(NetworkInteractionStore.ID, "modified_timestamp"),
                state_params=State(MatrixParametersStore.ID, "data"),
                state_dm=State(DistanceMatrixStore.ID, "data"),
                state_interaction=State(NetworkInteractionStore.ID, "data")
            )
        )
        @freezeargs
        @lru_cache
        def update_options_on_file_upload(ts_params, ts_dm, ts_interaction, state_params, state_dm, state_interaction):
            log_debug(f'{self.ID} - Updating matrix heatmap figure.')

            if ts_dm is None or not state_dm:
                log_debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # Record the duration
            start_time = time.time()

            # De-serialize the distance matrix store
            state_dm = DistanceMatrixStoreModel(**state_dm)
            params = MatrixParametersStoreModel(**state_params)
            state_interaction = NetworkInteractionStoreModel(**state_interaction)

            # If the metric is not set from the parameters, choose the first one
            if params.metric is None:
                feature_df = state_dm.get_files()[0].read()
            else:
                feature_df = state_dm.get_file(params.metric).read()

            # Subset the data visible if requested
            if params.sync_with_network is SyncWithNetwork.VISIBLE and len(state_interaction.nodes_visible) > 0:
                subset_cols = [x for x in feature_df.columns if x in state_interaction.nodes_visible]
                feature_df = feature_df.loc[subset_cols, subset_cols]
            elif params.sync_with_network is SyncWithNetwork.SELECTED and len(state_interaction.nodes_selected) > 0:
                subset_cols = [x for x in feature_df.columns if x in state_interaction.nodes_selected]
                feature_df = feature_df.loc[subset_cols, subset_cols]

            # if dataset in meta_dict.keys():
            #     meta_df = meta_dict[dataset]
            if len(params.slider) == 0:
                slidervals = [np.nanmin(feature_df.values), np.nanmax(feature_df.values)]
            else:
                slidervals = params.slider
            slidervals = sorted(slidervals)

            if len(params.slider) > 2:
                colorscale = []
                colors = get_color(params.color_scale, np.linspace(0, 1, len(slidervals) - 1))
                minval = min(slidervals)
                maxval = max(slidervals)
                normed_vals = [(x - minval) / (maxval - minval) for x in slidervals]
                for i, _ in enumerate(normed_vals[:-1]):
                    colorscale.append([normed_vals[i], colors[i]])
                    colorscale.append([normed_vals[i + 1], colors[i]])
            else:
                colorscale = params.color_scale

            heatmap = go.Heatmap(
                x=feature_df.columns,
                y=feature_df.index,
                z=feature_df,
                colorscale=colorscale,
                zmin=slidervals[0],
                zmax=slidervals[-1],
                name="",
            )

            fig = go.Figure(heatmap)
            fig.update_xaxes(
                tickangle=45,
                tickfont=dict(size=GRAPH_AXIS_FONT_SIZE),
                tickvals=np.arange(len(feature_df.columns)),
                ticktext=format_axis_labels(feature_df.columns)
            )
            fig.update_yaxes(
                tickfont=dict(size=GRAPH_AXIS_FONT_SIZE),
                tickvals=np.arange(len(feature_df.index)),
                ticktext=format_axis_labels(feature_df.index)
            )

            duration_s = time.time() - start_time
            log_debug(f'Finished creating distance matrix in {pretty_fmt_seconds(duration_s)}.')

            return dict(
                fig=fig
            )
