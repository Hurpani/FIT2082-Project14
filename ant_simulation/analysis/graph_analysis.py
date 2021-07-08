from typing import Union, List, Dict, Tuple
import matplotlib.pyplot as plt
import networkx as nx
import infomap
from matplotlib import colors


# Network drawing traits:
COLOURS: List[str] = ["#2596be", "#A985F0", "#23B030", "#D32A09", "#BAD1DA"]
OUTLINE: str = "#00040D"
WEIGHT: str = "weight"
COMMUNITY: str = "community"
INITIAL_AGE: str = "age"


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
    assoc_pseudoinv = list(map(lambda p: p[0], sorted(assoc_pseudoinv, key=lambda p: p[1])))[:count - 1]

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


def display_network(ntwrk: nx.Graph) -> nx.Graph:
    layout = nx.fruchterman_reingold_layout(ntwrk)
    communities_dict: Dict[str, int] = nx.get_node_attributes(ntwrk, COMMUNITY)
    colour_seq: List[str] = [COLOURS[i % len(COLOURS)] for i in communities_dict.values()]
    nx.draw_networkx_edges(ntwrk, pos=layout)
    nx.draw_networkx_nodes(ntwrk, pos=layout, node_color=colour_seq).set_edgecolor(
        colors.hex2color(OUTLINE)
    )
    plt.show()
    return ntwrk


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
    nx.set_node_attributes(ntwrk, coalesce_communities(id_corrected_communities(ntwrk, im), count, ntwrk), COMMUNITY)
    return ntwrk, im


def read_network(edge_file: str) -> Union[None, nx.Graph]:
    with open(edge_file) as edge_list:
        return nx.read_edgelist(edge_list)


def construct_network(interactions: List[str], density_factor: float = 0.25,
                      ages_dict: Dict[str, float] = {}) -> nx.Graph:
    ntwrk: Union[None, nx.Graph] = nx.parse_edgelist(interactions)
    if ntwrk is None or nx.number_of_edges(ntwrk) == 0:
        return nx.empty_graph()
    ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
    edge_list = sorted(ntwrk.edges, key=(lambda uv: ntwrk.get_edge_data(*uv, default=0)[WEIGHT]))
    i: int = 0
    while nx.density(ntwrk) > density_factor:
        if i >= len(edge_list):
            break
        ntwrk.remove_edge(*edge_list[i])
        ntwrk.remove_nodes_from(list(nx.isolates(ntwrk)))
        i += 1

    nx.set_node_attributes(ntwrk, values=ages_dict, name=INITIAL_AGE)

    return ntwrk

