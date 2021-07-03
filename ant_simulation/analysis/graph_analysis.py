from typing import Union, List
import matplotlib.pyplot as plt
import networkx as nx


def display_network(ntwrk: nx.Graph) -> None:
    nx.draw(ntwrk, nx.fruchterman_reingold_layout(ntwrk))
    plt.show()


# def find_communities(ntwrk: nx.Graph) -> None:
#     # Infomap community-finding algorithm: https://github.com/mapequation/infomap
#     pass


def gen_light_network(edge_file: str, density_factor: float = 0.25) -> nx.Graph:
    with open(edge_file) as edge_list:
        ntwrk: Union[None, nx.Graph] = nx.read_edgelist(edge_list)

    n: int = ntwrk.number_of_nodes()
    m: int = ntwrk.number_of_edges()

    if m == 0:
        return ntwrk

    # Find the floor(density_factor * n(n-1))th-order statistic.
    edge_weights: List[int] = sorted(map(lambda t: t[2], ntwrk.edges.data('weight', default=0)))

    k: int = int(density_factor * n * (n - 1))
    min_weight: int = max(edge_weights) if len(edge_weights) <= k else edge_weights[k]

    # Remove edges to satisfy the maximum edge density.
    for edge in ntwrk.edges:
        if ntwrk.get_edge_data(*edge, default=0)['weight'] < min_weight:
            ntwrk.remove_edge(*edge)

    # Remove isolated vertices.
    ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))

    return ntwrk
