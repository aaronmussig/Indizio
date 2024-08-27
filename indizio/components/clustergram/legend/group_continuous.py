from typing import List

import dash_bootstrap_components as dbc
from dash import html

from indizio.components.common.plotly_color_scale import CommonColorScale


class ClustergramLegendGroupContinuous(dbc.Card):
    ID = 'clustergram-legend-group-continuous'
    ID_COLOR_SCALE = f'{ID}-color-scale'
    ID_BINS = f'{ID}-bins'

    def __init__(self, group_name: str, bins: List[float], color_scale: str):
        # Create the rows for the table

        self.obj_color_scale = CommonColorScale(
            identifier={
                'type': self.ID_COLOR_SCALE,
                'group': group_name,
            },
            default_color=color_scale
        )

        super().__init__(
            className='mb-3',
            children=[
                dbc.CardHeader(
                    html.B(group_name)
                ),
                dbc.CardBody(
                    dbc.Table(
                        children=[
                            html.Thead(html.Tr([
                                html.Th("Bins", style={'width': '65%'}),
                                html.Th("Colour scale", style={'width': '35%'}),
                            ])),
                            html.Tbody(
                                children=[
                                    html.Tr([
                                        html.Td(
                                            dbc.Input(
                                                id={
                                                    'type': self.ID_BINS,
                                                    'group': group_name,
                                                },
                                                value=', '.join(map(str, bins)),
                                            )
                                        ),
                                        html.Td(
                                            self.obj_color_scale
                                        )
                                    ])
                                ]
                            ),
                        ],
                        hover=True,
                        size='sm',
                        className='mb-0'
                    )
                )
            ],
        )
