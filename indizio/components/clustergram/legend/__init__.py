import dash_bootstrap_components as dbc
from dash import Output, Input, State, html, callback

from indizio.components.clustergram.legend.container import ClustergramLegendContainer
from indizio.store.clustergram.legend import ClustergramLegendStore, ClustergramLegendStoreModel


class ClustergramLegendCanvas(html.Div):
    """
    This is the main card that wraps the Clustergram legend.
    """
    ID = "clustergram-legend-canvas"
    ID_TOGGLE_BTN = f'{ID}-toggle-btn'
    ID_CANVAS = f'{ID}-canvas'

    def __init__(self):
        super().__init__(
            children=[
                dbc.Button(
                    "Legend",
                    id=self.ID_TOGGLE_BTN,
                    n_clicks=0,
                ),
                dbc.Offcanvas(
                    id=self.ID_CANVAS,
                    className="network-properties-container",
                    style={
                        "minWidth": "800px"
                    },
                    scrollable=True,
                    title="Clustergram Legend",
                    is_open=False,
                    children=[
                        ClustergramLegendContainer()
                    ]
                ),
            ]
        )

        @callback(
            output=dict(
                is_open=Output(self.ID_CANVAS, "is_open"),
            ),
            inputs=dict(
                n1=Input(self.ID_TOGGLE_BTN, "n_clicks"),
                is_open=State(self.ID_CANVAS, "is_open"),
            ),
        )
        def toggle_network_form(n1, is_open):
            open_form = False
            if n1:
                open_form = not is_open
            return dict(
                is_open=open_form
            )

        @callback(
            output=dict(
                disabled=Output(self.ID_TOGGLE_BTN, "disabled"),
            ),
            inputs=dict(
                ts_legend=Input(ClustergramLegendStore.ID, "modified_timestamp"),
                state_legend=State(ClustergramLegendStore.ID, "data"),
            ),
        )
        def toggle_network_form(ts_legend, state_legend):
            disabled = True

            # If we have a state then check if a legend would exist
            if state_legend is not None:
                legend = ClustergramLegendStoreModel(**state_legend)
                disabled = legend.is_empty()

            return dict(
                disabled=disabled
            )
