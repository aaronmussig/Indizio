import logging
from functools import lru_cache

import dash_cytoscape as cyto
from dash import Output, Input, callback, State, html, dcc
from dash.exceptions import PreventUpdate

from indizio.components.network_properties import NetworkPropertiesCard
from indizio.store.distance_matrix import DistanceMatrixFileStore, DistanceMatrixFile
from indizio.store.dm_graph import DistanceMatrixGraphStore, DmGraph
from indizio.store.matrix_parameters import MatrixParametersStore, MatrixParameters, MatrixBinOption
from indizio.store.network_form_store import NetworkFormStore, NetworkFormStoreData
from indizio.util.cache import freezeargs, from_hashable
from indizio.util.graph import filter_graph
import plotly.graph_objects as go
import numpy as np

class MatrixPlot(dcc.Graph):
    """
    The cytoscape network graph component.
    """

    ID = 'matrix-plot'
    def __init__(self):
        super().__init__(
            id=self.ID,
            style={
                'width': 'min(calc(100vh - 150px), 100vw)',
                'height': 'min(calc(100vh - 150px), 100vw)'
            },
            responsive=True,
        )

        @callback(
            output=dict(
                fig=Output(self.ID, "figure"),
            ),
            inputs=dict(
                ts_params=Input(MatrixParametersStore.ID, "modified_timestamp"),
                ts_dm=Input(DistanceMatrixFileStore.ID, "modified_timestamp"),
                state_params=State(MatrixParametersStore.ID, "data"),
                state_dm=State(DistanceMatrixFileStore.ID, "data"),
            )
        )
        @freezeargs
        @lru_cache
        def update_options_on_file_upload(ts_params, ts_dm, state_params, state_dm):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating matrix heatmap figure.')

            if ts_dm is None or not state_dm:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialize the distance matrix
            print('TODO!@@!@!@!@')
            key = 'pa2.csv'

            fig = go.Figure()
            # empty initially

            # De-serialize the states
            feature_df = DistanceMatrixFile.deserialize(state_dm[key]).df
            params = MatrixParameters(**state_params)

            meta_df = None

            # if dataset in meta_dict.keys():
            #     meta_df = meta_dict[dataset]
            if len(params.slider) == 0:
                slidervals = [np.nanmin(feature_df.values), np.nanmax(feature_df.values)]
            else:
                slidervals = params.slider
            slidervals = sorted(slidervals)

            if params.bin_option is MatrixBinOption.BINNED:
                colorscale = []
                colors = get_color(scale, np.linspace(0, 1, len(slidervals) - 1))
                minval = min(slidervals)
                maxval = max(slidervals)
                normed_vals = [(x - minval) / (maxval - minval) for x in slidervals]
                for i, _ in enumerate(normed_vals[:-1]):
                    colorscale.append([normed_vals[i], colors[i]])
                    colorscale.append([normed_vals[i + 1], colors[i]])
            else:
                colorscale = params.color_scale

            ava_hm = go.Heatmap(
                x=feature_df.columns,
                y=feature_df.index,
                z=feature_df,
                colorscale=colorscale,
                zmin=slidervals[0],
                zmax=slidervals[-1],
                # colorbar=colorbar,
            )
            # if type(meta_df) != type(None):
            #     meta_hm = go.Heatmap(
            #         x=meta_df.columns,
            #         y=meta_df.index,
            #         z=meta_df,
            #         colorscale=colorscale,
            #         zmin=slidervals[0],
            #         zmax=slidervals[-1],
            #         showscale=False,
            #     )
            #     f1 = go.Figure(meta_hm)
            #     for data in f1.data:
            #         fig.add_trace(data)
            #
            #     f2 = go.Figure(ava_hm)
            #     for i in range(len(f2["data"])):
            #         f2["data"][i]["xaxis"] = "x2"
            #
            #     for data in f2.data:
            #         fig.add_trace(data)
            #
            #     fig.update_layout({"height": 800})
            #     fig.update_layout(
            #         xaxis={
            #             "domain": [0.0, 0.20],
            #             "mirror": False,
            #             "showgrid": False,
            #             "showline": False,
            #             "zeroline": False,
            #             # 'ticks':"",
            #             # 'showticklabels': False
            #         }
            #     )
            #     # Edit xaxis2
            #     fig.update_layout(
            #         xaxis2={
            #             "domain": [0.25, 1.0],
            #             "mirror": False,
            #             "showgrid": False,
            #             "showline": False,
            #             "zeroline": False,
            #             # 'showticklabels': False,
            #             # 'ticks':""
            #         }
            #     )
            # else:
            f = go.Figure(ava_hm)
            for data in f.data:
                fig.add_trace(data)
            fig.update_layout(
                xaxis={
                    "mirror": False,
                    "showgrid": False,
                    "showline": False,
                    "zeroline": False,
                    "tickmode": "array",
                    "ticktext": feature_df.columns.str.slice().to_list(),
                },
            )
            return dict(
                fig=fig
            )