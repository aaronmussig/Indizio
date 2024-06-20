from typing import Set

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE


class NetworkInteractionStoreModel(BaseModel):
    """
    This is the actual model for the data in the network interaction store.
    """

    nodes_selected: Set[str] = set()
    nodes_visible: Set[str] = set()

    def toggle_node(self, node_id: str):

        # Toggle the node active/inactive
        if node_id in self.nodes_selected:
            self.nodes_selected.remove(node_id)
        else:
            self.nodes_selected.add(node_id)

    def set_visible_nodes(self, nodes):
        self.nodes_visible = nodes


class NetworkInteractionStore(dcc.Store):
    """
    This class is used to represent the store for the network interaction.
    """
    ID = 'network-interaction-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=NetworkInteractionStoreModel().model_dump(mode='json')
        )
