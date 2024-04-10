import dash_bootstrap_components as dbc
from dash import html

from indizio.interfaces.bound import Bound
from indizio.store.network_form_store import NetworkParamThreshold


class NetworkThreshFilterItem(html.Tr):
    """
    This component is a general use row for threshold filtering.
    """

    ID = "network-thresh-filter-item"
    ID_LEFT_BOUND = f"{ID}-left-bound"
    ID_RIGHT_BOUND = f"{ID}-right-bound"
    ID_LEFT_VALUE = f"{ID}-left-value"
    ID_RIGHT_VALUE = f"{ID}-right-value"

    def __init__(self, threshold: NetworkParamThreshold):
        super().__init__(
            [
                html.Td(
                    f"{threshold.file_id}",
                ),
                html.Td(
                    dbc.Select(
                        id={
                            "type": self.ID_LEFT_BOUND,
                            "file_id": threshold.file_id
                        },
                        options=Bound.to_options(),
                        value=threshold.left_bound.value,
                        size='sm'
                    )
                ),
                html.Td(
                    dbc.Input(
                        id={
                            "type": self.ID_LEFT_VALUE,
                            "file_id": threshold.file_id
                        },
                        type="number",
                        value=threshold.left_value,
                        size='sm'
                    )
                ),
                html.Td(
                    dbc.Input(
                        id={
                            "type": self.ID_RIGHT_VALUE,
                            "file_id": threshold.file_id
                        },
                        type="number",
                        value=threshold.right_value,
                        size='sm'
                    )
                ),
                html.Td(
                    dbc.Select(
                        id={
                            "type": self.ID_RIGHT_BOUND,
                            "file_id": threshold.file_id
                        },
                        options=Bound.to_options(),
                        value=threshold.right_bound.value,
                        size='sm'
                    )
                )
            ]
        )
