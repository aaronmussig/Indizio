from typing import List, Dict

from indizio.store.network.interaction import NetworkInteractionStoreModel


class NetworkVizStyleSheet:
    """
    This is the default network stylesheet. This should be carefully modified
    as needed. It's instantiated as a class to faciliate this.

    Changes are made to this in order to display toggled nodes.
    """
    DEFAULT = {
        "node": {
            "width": "mapData(size, 0, 100, 15, 80)",
            "height": "mapData(size, 0, 100, 15, 80)",
            "background-color": "data(color)",
            "content": "data(label)",
        },
        "edge": {
            "opacity": 0.4
        },
    }

    def __init__(self, data=None):
        self.data = {**self.DEFAULT, **(data or {})}

    @classmethod
    def from_graph(cls, stylesheet):
        out = dict()
        for item in stylesheet:
            out[item['selector']] = item['style']
        return cls(out)

    def node_selected_key(self, node_id: str) -> str:
        return f'node[id = "{node_id}"]'

    def edge_selected_key(self, edge_id: str) -> str:
        return f'edge[id = "{edge_id}"]'

    def set_node_id_highlighted(self, node_id: str):
        node_key = self.node_selected_key(node_id)
        out = {
            "background-color": "#eb6864",
            "border-color": "#963835",
            "border-width": 2,
            "border-opacity": 1,
            "opacity": 1,
            "text-opacity": 1,
            "z-index": 9999,
        }
        self.data[node_key] = {**self.data.get(node_key, dict()), **out}

    def set_edge_id_highlighted(self, edge_id: str):
        edge_key = self.edge_selected_key(edge_id)
        new_data = {
            "line-color": "#eb6864",
            "opacity": 0.9,
            "z-index": 9000,
        }
        self.data[edge_key] = {**self.data.get(edge_key, dict()), **new_data}

    def deselect_node_id(self, node_id: str):
        node_key = self.node_selected_key(node_id)
        if node_key in self.data:
            self.data.pop(node_key)

    def deselect_edge_id(self, edge_id: str):
        edge_key = self.edge_selected_key(edge_id)
        if edge_key in self.data:
            self.data.pop(edge_key)

    def deselect_all(self):
        keys_to_remove = set()
        for key in self.data:
            if key.startswith('node[id') or key.startswith('edge[id'):
                keys_to_remove.add(key)
        for key in keys_to_remove:
            self.data.pop(key)

    def enable_edge_weights_text(self):
        self.data['edge']['content'] = 'data(label)'

    def disable_edge_weights_text(self):
        if 'content' in self.data['edge']:
            self.data['edge'].pop('content')

    def enable_edge_weights_thick(self):
        self.data['edge']['width'] = 'mapData(width, 0, 1, 1, 10)'

    def disable_edge_weights_thick(self):
        if 'width' in self.data['edge']:
            self.data['edge'].pop('width')

    def update_from_iteraction_store(self, store: NetworkInteractionStoreModel, edges: List[dict]):
        self.deselect_all()
        for node in store.nodes_selected:
            self.set_node_id_highlighted(node)
        for edge in edges:
            edge_data = edge['data']
            if edge_data['source'] in store.nodes_selected and edge_data['target'] in store.nodes_selected:
                self.set_edge_id_highlighted(edge_data['id'])

    def export(self) -> List[Dict]:
        out = list()
        for selector, style in self.data.items():
            out.append({
                'selector': selector,
                'style': style
            })
        return out
