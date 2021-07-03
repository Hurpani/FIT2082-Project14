from typing import Union, List, Dict, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import infomap
from matplotlib import colors


def id_corrected_communities(ntwrk: nx.Graph, im: infomap.Infomap) -> Dict["str", int]:
    """\
Given the InfoMap algorithm output, and the associated NetworkX network, returns
    a dictionary which maps a node's id to its associated community.
    """
    out_communities: Dict["str", int] = {}
    nodes: List[str] = list(ntwrk.nodes())
    communities: Dict[int, int] = im.get_modules()
    n: int = ntwrk.number_of_nodes()
    for i in range(n):
        out_communities[nodes[i]] = communities.get(i) - 1
    return out_communities


def display_network(ntwrk: nx.Graph, with_communities: Union[infomap.Infomap, None] = None) -> nx.Graph:
    layout = nx.fruchterman_reingold_layout(ntwrk)
    if with_communities is not None:
        communities_dict: Dict[str, int] = nx.get_node_attributes(ntwrk, "community")
        colour_seq: List[str] = [["#2596be", "#A985F0", "#23B030", "#D32A09"][i % 4] for i in communities_dict.values()]
        nx.draw_networkx_edges(ntwrk, pos=layout)
        nx.draw_networkx_nodes(ntwrk, pos=layout, node_color=colour_seq).set_edgecolor(
            colors.hex2color("#00040D")
        )
    else:
        nx.draw(ntwrk, pos=layout)
    plt.show()
    return ntwrk


def find_communities(ntwrk: nx.Graph) -> Tuple[nx.Graph, infomap.Infomap]:
    # Infomap community-finding algorithm: https://github.com/mapequation/infomap.
    # Requires version 1.4.0 or greater.
    im: infomap.Infomap = infomap.Infomap("--silent")
    im.add_networkx_graph(ntwrk)
    im.run()
    print(f"Discovered {im.num_top_modules} communities.")
    nx.set_node_attributes(ntwrk, id_corrected_communities(ntwrk, im), "community")
    return ntwrk, im


def gen_light_network(edge_file: str, density_factor: float = 0.25) -> nx.Graph:
    with open(edge_file) as edge_list:
        ntwrk: Union[None, nx.Graph] = nx.read_edgelist(edge_list)

    # Remove isolated vertices.
    ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))

    n: int = ntwrk.number_of_nodes()
    m: int = ntwrk.number_of_edges()

    if m == 0:
        return ntwrk

    # TODO: This is a difficult problem since it is possible for all edges to be of the same weight, and
    #  hence make it impossible to reach an edge density of 0.25.
    # Find the floor(0.5 * density_factor * n(n-1))th-order statistic.
    edge_weights: List[int] = sorted(map(lambda t: t[2], ntwrk.edges.data('weight', default=0)))
    k: int = int(0.5 * density_factor * n * (n - 1))
    min_weight: int = max(edge_weights) if len(edge_weights) <= k else edge_weights[k]

    # Remove edges to satisfy the maximum edge density.
    for edge in ntwrk.edges:
        if ntwrk.get_edge_data(*edge, default=0)['weight'] < min_weight:
            ntwrk.remove_edge(*edge)

    # Present the edge density:
    print(f"Expected edge density of at most {density_factor}. Actual density is {nx.density(ntwrk)}.")

    return ntwrk
