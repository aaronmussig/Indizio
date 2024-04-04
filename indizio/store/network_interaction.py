from typing import Optional, List, Set

from dash import dcc
from pydantic import BaseModel

from indizio.config import PERSISTENCE_TYPE


class NetworkInteractionData(BaseModel):
    """
    This is the actual model for the data in the network interaction store.
    """

    node_selected: Optional[str] = None
    edge_nodes: List[str] = list()

    def select_node(self, node: str):
        if node == self.node_selected:
            self.node_selected = None
        else:
            self.node_selected = node
        self.edge_nodes = list()

    def add_edge_node(self, node: str):
        self.edge_nodes.append(node)

    def has_node_selected(self) -> bool:
        return self.node_selected is not None

    def get_all_nodes(self) -> Set[str]:
        return set([self.node_selected] + self.edge_nodes)


class NetworkInteractionStore(dcc.Store):
    """
    This class is used to represent the store for the network interaction.
    """
    ID = 'network-interaction-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=NetworkInteractionData().model_dump(mode='json')
        )
