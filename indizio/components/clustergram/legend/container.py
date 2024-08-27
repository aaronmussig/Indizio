import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, html, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.legend.btn_update import ClustergramLegendUpdateButton
from indizio.components.clustergram.legend.group_continuous import ClustergramLegendGroupContinuous
from indizio.components.clustergram.legend.group_discrete import ClustergramLegendGroupDiscrete
from indizio.components.common.plotly_color_scale_discrete import get_name_to_colors, CommonColorScaleDiscrete
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel


class ClustergramLegendContainer(html.Div):
    ID = 'clustergram-legend-container'
    ID_DISCRETE = f'{ID}-discrete'
    ID_CONTINUOUS = f'{ID}-continuous'

    def __init__(self):
        super().__init__(
            [
                html.Div(id=self.ID_DISCRETE),
                html.Div(id=self.ID_CONTINUOUS),
                dbc.Row(
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



        @callback(
            output=dict(
                colors=Output({'type': ClustergramLegendGroupDiscrete.ID_COLOR_PICKER, 'group': ALL, 'key': ALL}, 'value'),
            ),
            inputs=dict(
                dropdown=Input({'type': ClustergramLegendGroupDiscrete.ID_COLOR_SCALE, 'group': ALL}, 'value'),
                prev_colors=State({'type': ClustergramLegendGroupDiscrete.ID_COLOR_PICKER, 'group': ALL, 'key': ALL}, 'value')
            ),
            prevent_initial_call=True
        )
        def update_on_select_change(dropdown, prev_colors):
            """
            Updates the degree filter item when the store is refreshed.
            """
            target_colour, target_group, target_type = None, None, None
            for group in ctx.args_grouping['dropdown']:
                if group['triggered']:
                    target_colour = group['value']
                    target_group = group['id']['group']
                    target_type = group['id']['type']

            # Skip if we didn't find a trigger
            if target_colour is None or target_group is None or target_type is None:
                raise PreventUpdate

            # Skip if there is no change required
            if target_colour == CommonColorScaleDiscrete.VALUE_NO_CHANGE:
                raise PreventUpdate

            # Get the previous values for all groups and keys
            d_prev_id_to_hex = dict()
            for prev_color in ctx.args_grouping['prev_colors']:
                str_id = f"{prev_color['id']['group']}-{prev_color['id']['key']}"
                d_prev_id_to_hex[str_id] = prev_color['value']

            # Load the colourscales
            d_colourscales = get_name_to_colors()
            avail_colours = d_colourscales[target_colour]
            next_colour_idx = 0

            # Match the output to be the correct group
            output = list()
            for out_group in ctx.outputs_grouping['colors']:
                id_out_group = out_group['id']['group']
                str_id = f"{id_out_group}-{out_group['id']['key']}"
                prev_color = d_prev_id_to_hex[str_id]

                if id_out_group == target_group:
                    output.append(avail_colours[next_colour_idx % len(avail_colours)])
                    next_colour_idx += 1
                else:
                    output.append(prev_color)

            return dict(
                colors=output
            )
