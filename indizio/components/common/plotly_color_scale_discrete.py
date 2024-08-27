import inspect
import re
import plotly.express as px
from dash import dcc, html

from indizio.util.plot import rgb_tuple_to_hex

RE_RGB = re.compile(r'rgba?\(([\d.]+), ?([\d.]+), ?([\d.]+)(?:, ?([\d.])+)?\)')

class CommonColorScaleDiscrete(dcc.Dropdown):
    """
    This component contains the color scale dropdown.
    """

    VALUE_NO_CHANGE = 'NO_CHANGE'

    def __init__(self, identifier, default_color: str, show_none: bool=True):
        self.ID = identifier
        super().__init__(
            id=self.ID,
            options=get_options_for_colorscale(show_none),
            value=default_color,
            className="bg-light text-dark",
            clearable=False
        )


def get_name_to_colors():
    # Get the module names from the qualitative colours
    colorscales = dict()
    for name, obj in inspect.getmembers(px.colors.qualitative):
        if not name.startswith('__') and isinstance(obj, list) and len(obj) > 3:
            cur_colors = list()
            # Convert any non-hex colours to hex
            for cur_color in obj:
                if cur_color.startswith('#'):
                    cur_colors.append(cur_color)
                elif cur_color.startswith('rgb'):
                    match = RE_RGB.match(cur_color)
                    rgb = float(match.group(1)), float(match.group(2)), float(match.group(3))
                    cur_colors.append(rgb_tuple_to_hex(rgb))
            colorscales[name] = cur_colors
    return colorscales


def get_options_for_colorscale(show_none: bool):
    out = list()
    if show_none:
        out.append(dict(
            label='No change',
            value=CommonColorScaleDiscrete.VALUE_NO_CHANGE
        ))

    colorscales = get_name_to_colors()

    for colorscale_name, colors in colorscales.items():
        stop_spacing = 100 / len(colors)
        stop_margin = stop_spacing * 0.01

        # Convert the colorscale into RGB values for the gradient
        gradient_stops = list()
        for color_i in range(1, len(colors)):
            prev_color = colors[color_i - 1]
            cur_color = colors[color_i]

            cur_stop = stop_spacing * color_i

            gradient_stops.append(f'{prev_color} {cur_stop}%')
            gradient_stops.append(f'{cur_color} {cur_stop + stop_margin}%')

        gradient_stops_str = ', '.join(gradient_stops)

        out.append(dict(
            label=html.Div(
                style=dict(
                    display='flex',
                ),
                children=[
                    html.Div(
                        children=[
                            colorscale_name
                        ],
                        style=dict(
                            display='flex'
                        )
                    ),
                    html.Div(
                        style=dict(
                            height='20px',
                            marginLeft='20px',
                            marginRight='20px',
                            marginTop='auto',
                            marginBottom='auto',
                            width='100%',
                            minWidth='100px',
                            display='flex',
                            borderRadius='5px',
                            background=f'linear-gradient(90deg, {gradient_stops_str})',
                        )
                    )
                ]
            ),
            value=colorscale_name
        ))

    return out
