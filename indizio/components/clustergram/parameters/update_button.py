import logging
from typing import List

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Output, Input, callback, ctx, State
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.parameters import ClustergramParamsMetric, ClustergramParamsTree, \
    ClustergramParamsMetadata, ClustergramParamsClusterOn, ClustergramParamsOptimalLeafOrder, \
    ClustergramParamsSyncWithNetwork
from indizio.models.clustergram.cluster_on import ClusterOn
from indizio.models.clustergram.legend import LegendItem, LegendGroup
from indizio.models.common.boolean import BooleanYesNo
from indizio.models.common.sync_with_network import SyncWithNetwork
from indizio.models.metadata.metadata_column import MetadataColumn
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel
from indizio.store.clustergram.parameters import ClustergramParametersStore, ClustergramParametersStoreModel
from indizio.store.metadata_file import MetadataFileStoreModel, MetadataFileStore


class ClustergramParamsUpdateButton(dbc.Button):
    """
    This component will store the Clustergram parameters in the store.
    """

    ID = "clustergram-params-update-button"

    def __init__(self):
        super().__init__(
            "Update Clustergram",
            id=self.ID,
            color="success",
            n_clicks=0,
        )

        @callback(
            output=dict(
                params=Output(ClustergramParametersStore.ID, "data"),
                legend=Output(ClustergramLegendStore.ID, "data", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                metric=Input(ClustergramParamsMetric.ID, "value"),
                tree=Input(ClustergramParamsTree.ID, 'value'),
                metadata=Input(ClustergramParamsMetadata.ID, 'value'),
                cluster_on=Input(ClustergramParamsClusterOn.ID, 'value'),
                optimal_leaf_ordering=Input(ClustergramParamsOptimalLeafOrder.ID, 'value'),
                metadata_cols=Input(ClustergramParamsMetadata.ID_COLS, 'value'),
                sync_with_network=Input(ClustergramParamsSyncWithNetwork.ID, 'value'),
                state_legend=State(ClustergramLegendStore.ID, 'data'),
                state_meta=State(MetadataFileStore.ID, "data"),
            ),
            prevent_initial_call=True
        )
        def update_options_on_file_upload(n_clicks, metric, tree, metadata, cluster_on, optimal_leaf_ordering,
                                          metadata_cols, sync_with_network, state_legend, state_meta):
            log = logging.getLogger()
            log.debug(f'{self.ID} - Updating clustergram visualization parameters.')

            if not n_clicks or ctx.triggered_id != self.ID:
                log.debug(f'{self.ID} - No data to update from.')
                raise PreventUpdate

            # De-serialise the legend data
            state_legend = ClustergramLegendStoreModel(**state_legend)
            state_meta = MetadataFileStoreModel(**state_meta)

            # For some reason putting this legend-updating code in the main
            # clustergram method throws an error, so it's here instead.

            # If there are metadata columns, read the metadata file and assign
            # colours to each value
            if metadata and metadata_cols:
                # Read the metadata file
                df_meta = state_meta.get_file(metadata).read()

                # Generate the new legend and set it to be current
                state_legend = set_legend(df_meta, metadata_cols, state_legend)

            return dict(
                params=ClustergramParametersStoreModel(
                    metric=metric,
                    tree=tree,
                    metadata=metadata,
                    cluster_on=ClusterOn(cluster_on),
                    optimal_leaf_order=BooleanYesNo(optimal_leaf_ordering),
                    metadata_cols=metadata_cols if metadata_cols else list(),
                    sync_with_network=SyncWithNetwork(sync_with_network)
                ).model_dump(mode='json'),
                legend=state_legend.model_dump(mode='json')
            )


def set_legend(df_meta: pd.DataFrame, columns: List[str],
               old_legend: ClustergramLegendStoreModel) -> ClustergramLegendStoreModel:
    """
    This method generates the legend store based on the metadata & columns.
    """

    # Create a new legend
    legend = ClustergramLegendStoreModel()

    # Process each metadata column
    for col in columns:

        # Convert the values in the column to a dictionary
        cur_col = MetadataColumn(df_meta[col])
        cur_group = LegendGroup(name=col)

        # Check if this is a continuous or discrete column
        if cur_col.is_discrete():

            unique_values = cur_col.unique_values()

            # Generate a list of hex codes to sample from
            hex_colours = tuple(px.colors.qualitative.Light24)
            hex_colours_len = len(hex_colours)
            hex_next_idx = 0

            # Assign an index and colour to each value
            for value in sorted(unique_values):
                if value == MetadataColumn.MISSING_VALUE_DISCRETE:
                    cur_colour = MetadataColumn.MISSING_HEX
                else:
                    cur_colour = hex_colours[hex_next_idx % hex_colours_len]
                    hex_next_idx += 1
                new_item = LegendItem(
                    text=value,
                    hex_code=cur_colour
                )
                cur_group.discrete_bins[value] = new_item

        # Continuous values
        else:
            # Normalise the values between what has been allocated
            cur_col_min, cur_col_max = cur_col.get_min_max()

            # Simply save this
            cur_group.continuous_bins = [cur_col_min, cur_col_max]
            cur_group.continuous_colorscale = 'agsunset'

        # Save the current group to the legend store
        legend.groups[col] = cur_group

    return legend
