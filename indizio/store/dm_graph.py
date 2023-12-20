import logging
from typing import List

import networkx as nx
import numpy as np
from dash import dcc
from pydantic import BaseModel
from tqdm import tqdm

from indizio.config import PERSISTENCE_TYPE
from indizio.store.distance_matrix import DistanceMatrixFile


class DmGraph(BaseModel):
    graph: nx.Graph

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def from_distance_matricies(cls, matrices: List[DistanceMatrixFile]):
        log = logging.getLogger()

        G = nx.Graph()
        # add edges first
        edge_dfs = []
        edge_attrs = []
        for dm in matrices:
            edge_attrs.append(dm.file_name)
            edge_dfs.append(dm.df)

        # Make sure the dfs are all same shapes
        assert len(list(set([df.shape[0] for df in edge_dfs]))) == 1
        assert len(list(set([df.shape[1] for df in edge_dfs]))) == 1

        stacked = [frame.where(np.triu(np.ones(frame.shape)).astype(bool)).stack() for frame in edge_dfs]
        pairs = stacked[0].index
        log.debug("Constructing nodes. . .")
        nodes = list(edge_dfs[0].columns)

        for node in tqdm(nodes):
            G.add_node(node)

        log.debug("Constructing edges. . .")
        # edges = []
        data = list(zip(edge_attrs, stacked))
        edge_dict = {k: dict() for k in pairs}
        for tup in tqdm(pairs):
            for attribute, df in data:
                edge_dict[tup][attribute] = df.loc[tup]

        edges = [(*k, v) for k, v in edge_dict.items()]
        G.add_edges_from(edges)
        # Need to add the metadata...

        return cls(graph=G)

    def serialize(self):
        return {'graph': nx.cytoscape_data(self.graph)}

    @classmethod
    def deserialize(cls, data):
        return cls(graph=nx.cytoscape_graph(data['graph']))


class DistanceMatrixGraphStore(dcc.Store):
    ID = 'distance-matrix-graph-store'

    def __init__(self):
        super().__init__(
            id=self.ID,
            storage_type=PERSISTENCE_TYPE,
            data=None
        )
