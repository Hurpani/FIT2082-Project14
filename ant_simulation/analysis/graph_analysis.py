from typing import Union, List, Dict, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import infomap
from matplotlib import colors


class EmptyNetworkException(Exception):
    """\
This exception is raised when we attempt to process an empty
    network, where no output is sensible.
    """
    pass


def coalesce_communities(comm_map: Dict[str, int], count: int,
                         ntwrk: Union[None, nx.Graph] = None) -> Dict[str, int]:
    """\
Given a community mapping, finds the (count-1)-largest communities, and then
    groups together the remaining ones to form a count-community mapping.

    If count is non-positive, then no changes are made.
    """
    if count <= 0:
        return comm_map

    # Maps a community to its count.
    pseudoinv: List[int] = []

    def increment(i: int, lst=pseudoinv) -> None:
        if i >= len(lst):
            lst += ([0] * (i - len(lst) + 1))
        lst[i] += 1

    if ntwrk is not None:
        # Iterate over the vertices in the network. :)
        for node in ntwrk.nodes:
            increment(comm_map[node])
    else:
        # Iterate over the dictionary instead. :(
        for c in comm_map.values():
            increment(c)

    # Construct a list of the (count-1)-largest communities.
    assoc_pseudoinv: List[Tuple[int, int]] = []
    for i in range(len(pseudoinv)):
        assoc_pseudoinv.append((i, pseudoinv[i]))
    assoc_pseudoinv = list(map(lambda p: p[0], sorted(assoc_pseudoinv, key=lambda p: p[1])))[:count]

    outmap: Dict[str, int] = {}
    if ntwrk is not None:
        for node in ntwrk.nodes:
            outmap[node] = comm_map[node] if comm_map[node] in assoc_pseudoinv else count - 1
    else:
        for k, v in comm_map.values():
            outmap[k] = v if v in assoc_pseudoinv else count - 1
    return outmap


def id_corrected_communities(ntwrk: nx.Graph, im: infomap.Infomap) -> Dict[str, int]:
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


def display_network(ntwrk: nx.Graph, with_communities: Union[infomap.Infomap, None] = None) -> \
        Tuple[nx.Graph, Union[infomap.Infomap, None]]:
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
    return ntwrk, with_communities


def find_communities(ntwrk: nx.Graph, count: int = -1, verbose: bool = False) -> Tuple[nx.Graph, infomap.Infomap]:
    """\
Applies the Infomap community-finding algorithm. If the specified count is non-positive,
    then no coalescing of communities occurs; otherwise, only the (count-1)-largest
    communities remain distinct.
    """
    # Infomap community-finding algorithm: https://github.com/mapequation/infomap.
    # Requires version 1.4.0 or greater.
    if ntwrk is None or ntwrk.number_of_nodes() == 0:
        raise EmptyNetworkException()
    im: infomap.Infomap = infomap.Infomap("--silent")
    im.add_networkx_graph(ntwrk)
    im.run()
    if verbose:
        print(f"Discovered {im.num_top_modules} communities.")
    nx.set_node_attributes(ntwrk, coalesce_communities(id_corrected_communities(ntwrk, im), count, ntwrk), "community")
    return ntwrk, im


def read_network(edge_file: str) -> Union[None, nx.Graph]:
    with open(edge_file) as edge_list:
        return nx.read_edgelist(edge_list)


def construct_network(interactions: List[str], density_factor: float = 0.25) -> nx.Graph:
    ntwrk: Union[None, nx.Graph] = nx.parse_edgelist(interactions)
    if ntwrk is None or nx.number_of_edges(ntwrk) == 0:
        return nx.empty_graph()
    ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
    edge_list = sorted(ntwrk.edges, key=(lambda uv: ntwrk.get_edge_data(*uv, default=0)['weight']))
    i: int = 0
    while nx.density(ntwrk) > density_factor:
        if i >= len(edge_list):
            break
        ntwrk.remove_edge(*edge_list[i])
        ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
        i += 1

    return ntwrk


# def iterative_gen_light_network(edge_file: str, density_factor: float = 0.25) -> nx.Graph:
#     ntwrk: Union[None, nx.Graph] = read_network(edge_file)
#     if ntwrk is None or nx.number_of_edges(ntwrk) == 0:
#         return nx.empty_graph()
#     ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
#     edge_list = sorted(ntwrk.edges, key=(lambda uv: ntwrk.get_edge_data(*uv, default=0)['weight']))
#     i: int = 0
#     while nx.density(ntwrk) > density_factor:
#         if i >= len(edge_list):
#             break
#         ntwrk.remove_edge(*edge_list[i])
#         ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
#         i += 1
#
#     return ntwrk


# def gen_light_network(edge_file: str, density_factor: float = 0.25) -> nx.Graph:
#     ntwrk: Union[None, nx.Graph] = read_network(edge_file)
#
#     # Remove isolated vertices.
#     ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
#
#     n: int = ntwrk.number_of_nodes()
#     m: int = ntwrk.number_of_edges()
#
#     if m == 0:
#         return ntwrk
#
#     # NOTE: This is a difficult problem since it is possible for all edges to be of the same weight, and
#     #  hence make it impossible to reach an edge density of 0.25.
#     # Find the floor(0.5 * density_factor * n(n-1))th-order statistic.
#     edge_weights: List[int] = sorted(map(lambda t: t[2], ntwrk.edges.data('weight', default=0)))
#     k: int = int(0.5 * density_factor * n * (n - 1))
#     min_weight: int = max(edge_weights) if len(edge_weights) <= k else edge_weights[k]
#
#     # Remove edges to satisfy the maximum edge density.
#     for edge in ntwrk.edges:
#         if ntwrk.get_edge_data(*edge, default=0)['weight'] < min_weight:
#             ntwrk.remove_edge(*edge)
#
#     # Remove isolated vertices after the reduction.
#     ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
#
#     # Present the edge density:
#     # print(f"Expected edge density of at most {density_factor}. Actual density is {nx.density(ntwrk)}.")
#
#     return ntwrk
