import dash_bootstrap_components as dbc
from dash import Output, Input, callback, State, ALL, ctx
from dash.exceptions import PreventUpdate

from indizio.components.clustergram.legend.group_continuous import ClustergramLegendGroupContinuous
from indizio.components.clustergram.legend.group_discrete import ClustergramLegendGroupDiscrete
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel


class ClustergramLegendUpdateButton(dbc.Button):
    ID = 'clustergram-legend-update-button'

    def __init__(self):

        super().__init__(
            "Update Legend",
            id=self.ID,
            color="success",
            n_clicks=0,
        )

        @callback(
            output=dict(
                legend=Output(ClustergramLegendStore.ID, 'data', allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                state_legend=State(ClustergramLegendStore.ID, "data"),
                discrete_colors=State(
                    {'type': ClustergramLegendGroupDiscrete.ID_COLOR_PICKER, 'group': ALL, 'key': ALL}, 'value'),
                continuous_bins=State({'type': ClustergramLegendGroupContinuous.ID_BINS, 'group': ALL}, 'value'),
                continuous_colors=State({'type': ClustergramLegendGroupContinuous.ID_COLOR_SCALE, 'group': ALL},
                                        'value'),
            ),
            prevent_initial_call=True
        )
        def update_on_button_press(n_clicks, state_legend, discrete_colors, continuous_bins, continuous_colors):
            """
            Updates the degree filter item when the store is refreshed.
            """
            if not n_clicks or state_legend is None:
                raise PreventUpdate

            # Load the state
            legend = ClustergramLegendStoreModel(**state_legend)

            # Extract the hex colours for each discrete group
            for color_group in ctx.args_grouping['discrete_colors']:
                group_name = color_group['id']['group']
                key_name = color_group['id']['key']
                hex_code = color_group['value']
                legend.set_discrete_group_hex(group_name, key_name, hex_code)

            # Extract the continuous color info
            for bin_group in ctx.args_grouping['continuous_bins']:
                group_name = bin_group['id']['group']
                bins = bin_group['value']

                # Convert the bins to a list of floats
                new_bins = list()
                for bin_str in bins.split(','):
                    new_bins.append(float(bin_str))
                new_bins.sort()

                legend.set_continuous_group_bins(group_name, new_bins)

            for color_group in ctx.args_grouping['continuous_colors']:
                group_name = color_group['id']['group']
                colorscale = color_group['value']
                legend.set_continuous_group_colorscale(group_name, colorscale)

            return dict(
                legend=legend.model_dump(mode='json'),
            )
