from functools import lru_cache

import dash
from dash import html, callback, Output, Input

from indizio import config
from indizio.cache import CACHE_MANAGER
from indizio.components.upload_form import UploadFormContainer
from indizio.components.uploaded_files import UploadedFileContainer

import time

from indizio.util.cache import cache_by

dash.register_page(__name__, path='/', name=config.PAGE_TITLE)

layout = html.Div([
    html.H1('INDEX'),
    html.Div('This is our Home page content.'),
    UploadFormContainer(),
    # html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
    #     html.Button(id="button_id", children="Run Job!"),
    #     html.Button(id="cancel_button_id", children="Cancel Running Job!"),
])

# @callback(
#     output=(Output("paragraph_id", "children"), Output("button_id", "n_clicks")),
#     inputs=Input("button_id", "n_clicks"),
#     running=[
#         (Output("button_id", "disabled"), True, False),
#         (Output("cancel_button_id", "disabled"), False, True),
#     ],
#     cancel=[Input("cancel_button_id", "n_clicks")],
#     background=True,
#     manager=CACHE_MANAGER,
# )
# def callback(n_clicks):
#     return do_callback(n_clicks=n_clicks)
#
#
# # @cache_by('n_clicks')
# def do_callback(n_clicks):
#     print('called', n_clicks)
#     time.sleep(10)
#     return [f"Clicked {n_clicks} times"], (n_clicks or 0) % 2
