import plotly.express as px
from dash import dcc, html


class CommonColorScale(dcc.Dropdown):
    """
    This component contains the color scale dropdown.
    """

    def __init__(self, identifier, default_color: str):
        self.ID = identifier
        super().__init__(
            id=self.ID,
            options=get_options_for_colorscale(),
            value=default_color,
            className="bg-light text-dark",
            clearable=False
        )


def get_options_for_colorscale():
    out = list()
    for colorscale_name in px.colors.named_colorscales():
        colorscale = px.colors.get_colorscale(colorscale_name)

        # Convert the colorscale into RGB values for the gradient
        gradient_stops = list()
        for color_stop_prop, color in colorscale:
            color_stop_pct = color_stop_prop * 100
            gradient_stops.append(f'{color} {color_stop_pct}%')
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
