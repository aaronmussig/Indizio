import json

import dash_bootstrap_components as dbc
from dash import callback, Output, Input, State, html


class DebugStore(dbc.Card):
    ID_PREFIX = 'debug-store'

    def __init__(self, target_store_id: str):
        id_store = f'{self.ID_PREFIX}-{target_store_id}-store'

        super().__init__(
            style={'marginBottom': '10px'},
            children=[
                dbc.CardHeader(html.B(f'{target_store_id}')),
                dbc.CardBody(
                    html.Code(
                        id=id_store,
                        style={
                            'lineHeight': '0',
                            'fontSize': '12px',
                        }
                    )
                )
            ]
        )

        @callback(
            output=dict(
                out=Output(id_store, "children"),
            ),
            inputs=dict(
                ts=Input(target_store_id, "modified_timestamp"),
                store=State(target_store_id, "data"),
            )
        )
        def upload_on_store_change(ts, store):
            indent = 4
            json_str = json.dumps(store, indent=indent)

            output = list()
            for line in json_str.split('\n'):
                line_len_without_indent = len(line.lstrip())
                n_indents = (len(line) - line_len_without_indent) // indent
                output.append(
                    html.P(
                        children=[line],
                        style={'marginLeft': f'{n_indents * 20}px'}
                    )
                )

            return dict(
                out=output
            )
