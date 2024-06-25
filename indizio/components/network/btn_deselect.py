import dash_bootstrap_components as dbc
from dash import Output, Input, callback, html, State
from dash.exceptions import PreventUpdate

from indizio.store.network.interaction import NetworkInteractionStore, NetworkInteractionStoreModel


class NetworkBtnDeselect(html.Div):
    """
    This component is the "Download as GraphML" button.
    """

    ID = "network-deselect-button"

    def __init__(self):
        super().__init__(
            [
                dbc.Button(
                    "Deselect nodes",
                    id=self.ID,
                    color="primary"
                ),
            ],
            style={'marginLeft': '10px'}
        )

        @callback(
            output=dict(
                interaction_state=Output(NetworkInteractionStore.ID, "data", allow_duplicate=True),
            ),
            inputs=dict(
                n_clicks=Input(self.ID, "n_clicks"),
                interaction_state=State(NetworkInteractionStore.ID, "data"),
            ),
            prevent_initial_call=True,
        )
        def on_click(n_clicks, interaction_state):
            if not n_clicks:
                raise PreventUpdate

            # De-serialize the states
            state = NetworkInteractionStoreModel(**interaction_state)
            state.deselect_nodes()

            # Return the data
            return dict(
                interaction_state=state.model_dump(mode='json')
            )
