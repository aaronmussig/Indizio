from typing import Dict

import dash_bootstrap_components as dbc
from dash import html

from indizio.components.common.plotly_color_scale_discrete import CommonColorScaleDiscrete
from indizio.models.clustergram.legend import LegendItem


class ClustergramLegendGroupDiscrete(dbc.Card):
    ID = 'clustergram-legend-group-discrete'
    ID_COLOR_PICKER = f'{ID}-color-picker'
    ID_COLOR_SCALE = f'{ID}-color-scale'

    def __init__(self, group_name: str, bins: Dict[str, LegendItem]):
        # Create the rows for the table
        rows = list()
        for current_bin in bins.values():
            rows.append(
                html.Tr([
                    html.Td(current_bin.text),
                    html.Td(
                        dbc.Input(
                            type="color",
                            id={
                                'type': self.ID_COLOR_PICKER,
                                'group': group_name,
                                'key': current_bin.text,
                            },
                            value=current_bin.hex_code,
                        ),
                    )
                ])
            )
        rows.append(
            html.Tr([
                html.Td(html.B('Replace all:')),
                html.Td(
                    CommonColorScaleDiscrete(
                        {'type': self.ID_COLOR_SCALE, 'group': group_name},
                        'NO_CHANGE'
                    )
                )
            ])
        )

        super().__init__(
            className='mb-3',

            children=[
                dbc.CardHeader([
                    html.B(group_name),
                ],

                ),
                dbc.CardBody(
                    dbc.Table(
                        children=[
                            html.Thead(html.Tr([
                                html.Th("Value", style={'width': '65%'}),
                                html.Th("Colour", style={'width': '35%'}),
                            ])),
                            html.Tbody(
                                children=rows
                            ),
                        ],
                        hover=True,
                        size='sm',
                        className='mb-0'
                    )
                ),
            ],
        )
