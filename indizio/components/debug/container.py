from dash import html

from indizio.components.debug.store import DebugStore
from indizio.store.active_stores import ACTIVE_STORES


class DebugContainer(html.Div):

    def __init__(self):
        super().__init__(
            children=[DebugStore(x.ID) for x in ACTIVE_STORES]
        )

