import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html

from indizio.components.clustergram.legend.btn_update import ClustergramLegendUpdateButton
from indizio.components.clustergram.legend.group_continuous import ClustergramLegendGroupContinuous
from indizio.components.clustergram.legend.group_discrete import ClustergramLegendGroupDiscrete
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel


class ClustergramLegendContainer(html.Div):
    ID = 'clustergram-legend-container'
    ID_DISCRETE = f'{ID}-discrete'
    ID_CONTINUOUS = f'{ID}-continuous'

    def __init__(self):
        super().__init__(
            [
                dbc.Row(id=self.ID_DISCRETE),
                dbc.Row(id=self.ID_CONTINUOUS),
                dbc.Row(
                    className='mt-2',
                    children=[ClustergramLegendUpdateButton()]
                )
            ]
        )

        @callback(
            output=dict(
                discrete=Output(self.ID_DISCRETE, "children"),
                continuous=Output(self.ID_CONTINUOUS, "children"),
            ),
            inputs=dict(
                ts_legend=Input(ClustergramLegendStore.ID, "modified_timestamp"),
                state_legend=State(ClustergramLegendStore.ID, "data"),
            ),
        )
        def populate(ts_legend, state_legend):

            # Load the legend
            legend = ClustergramLegendStoreModel(**state_legend)

            # Process each group
            discrete, continuous = list(), list()
            for group in legend.groups.values():

                # If the group is discrete, create the items
                if group.is_discrete():
                    discrete.append(
                        ClustergramLegendGroupDiscrete(
                            group_name=group.name,
                            bins=group.discrete_bins
                        )
                    )

                # If the group is continuous, create the items
                if group.is_continuous():
                    continuous.append(
                        ClustergramLegendGroupContinuous(
                            group_name=group.name,
                            bins=group.continuous_bins,
                            color_scale=group.continuous_colorscale
                        )
                    )

            return dict(
                discrete=discrete,
                continuous=continuous
            )
