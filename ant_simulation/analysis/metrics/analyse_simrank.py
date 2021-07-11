from typing import List, Dict
import networkx as nx
import numpy as np


SIMRANK_TITLE: str = "***SIMRANK***"


def simrank__write_out(ntwrk: nx.Graph) -> str:
    return f"{SIMRANK_TITLE}\n{gen_simrank(ntwrk)}"


def gen_simrank(ntwrk: nx.Graph) -> np.array:
    nodes: List[str] = list(ntwrk.nodes)
    n: int = len(nodes)
    out_array: np.array = np.zeros((n, n))
    sr: Dict[str, Dict[str, float]] = nx.simrank_similarity(ntwrk)
    nodes_to_index: Dict[str, int] = {}
    for i in range(n):
        nodes_to_index[nodes[i]] = i
    for u in nodes:
        for v in nodes:
            out_array[nodes_to_index[u], nodes_to_index[v]] = sr[u][v]
    return out_array
