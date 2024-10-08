from typing import Tuple

import plotly
import plotly.express as px
from PIL import ImageColor
from _plotly_utils.basevalidators import ColorscaleValidator
import numpy as np


################################################################################
## These two color functions from                                             ##
## https://stackoverflow.com/questions/62710057/access-color-from-plotly-color-scale
################################################################################
def get_color(colorscale_name, loc):
    # first parameter: Name of the property being validated
    # second parameter: a string, doesn't really matter in our use case
    cv = ColorscaleValidator("colorscale", "")
    # colorscale will be a list of lists: [[loc1, "rgb1"], [loc2, "rgb2"], ...]
    colorscale = cv.validate_coerce(colorscale_name)

    if hasattr(loc, "__iter__"):
        return [get_continuous_color(colorscale, x) for x in loc]
    return get_continuous_color(colorscale, loc)


def get_continuous_color(colorscale, intermed):
    """
    Plotly continuous colorscales assign colors to the range [0, 1]. This function computes the intermediate
    color for any value in that range.

    Plotly doesn't make the colorscales directly accessible in a common format.
    Some are ready to use:

        colorscale = plotly.colors.PLOTLY_SCALES["Greens"]

    Others are just swatches that need to be constructed into a colorscale:

        viridis_colors, scale = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
        colorscale = plotly.colors.make_colorscale(viridis_colors, scale=scale)

    :param colorscale: A plotly continuous colorscale defined with RGB string colors.
    :param intermed: value in the range [0, 1]
    :return: color in rgb string format
    :rtype: str
    """
    if len(colorscale) < 1:
        raise ValueError("colorscale must have at least one color")

    hex_to_rgb = lambda c: "rgb" + str(ImageColor.getcolor(c, "RGB"))

    if intermed <= 0 or len(colorscale) == 1:
        c = colorscale[0][1]
        return c if c[0] != "#" else hex_to_rgb(c)
    if intermed >= 1:
        c = colorscale[-1][1]
        return c if c[0] != "#" else hex_to_rgb(c)

    for cutoff, color in colorscale:
        if intermed > cutoff:
            low_cutoff, low_color = cutoff, color
        else:
            high_cutoff, high_color = cutoff, color
            break

    if (low_color[0] == "#") or (high_color[0] == "#"):
        # some color scale names (such as cividis) returns:
        # [[loc1, "hex1"], [loc2, "hex2"], ...]
        low_color = hex_to_rgb(low_color)
        high_color = hex_to_rgb(high_color)

    return plotly.colors.find_intermediate_color(
        lowcolor=low_color,
        highcolor=high_color,
        intermed=((intermed - low_cutoff) / (high_cutoff - low_cutoff)),
        colortype="rgb",
    )


def numerical_colorscale(values, colorscale):
    # Normalize the values between 0 and 1
    cur_min = min(values)
    cur_max = max(values)
    cur_range = cur_max - cur_min
    d_val_to_norm = {x: (x - cur_min) / cur_range for x in values}

    d_val_to_hex = {
        k: rgb_tuple_to_hex(px.colors.sample_colorscale(colorscale, samplepoints=[v], colortype='tuple')[0])
        for k, v in d_val_to_norm.items()
    }

    return d_val_to_hex

def categorical_colorscale(values, colorscale=px.colors.qualitative.Dark24):
    unq_values = list()
    seen = set()
    for value in values:
        if value not in seen:
            unq_values.append(value)
            seen.add(value)
    out = dict()
    for i, value in enumerate(unq_values):
        if isinstance(value, float) and value is np.isnan(value):
            color = '#FFFFFF'
        else:
            color = colorscale[i % len(colorscale)]
        out[value] = color
    return out



def rgb_tuple_to_hex(rgb: Tuple[int, int, int]) -> str:
    if any(x > 1 for x in rgb):
        red = min(int(rgb[0]), 255)
        green = min(int(rgb[1]), 255)
        blue = min(int(rgb[2]), 255)
    else:
        red = min(int(rgb[0] * 255), 255)
        green = min(int(rgb[1] * 255), 255)
        blue = min(int(rgb[2] * 255), 255)
    return '#{:02x}{:02x}{:02x}'.format(red, green, blue)
