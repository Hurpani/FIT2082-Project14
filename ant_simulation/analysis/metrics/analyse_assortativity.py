from typing import List, Tuple, NamedTuple
import networkx as nx
from ant_simulation.analysis.graph_analysis import COMMUNITY, INITIAL_AGE
from itertools import groupby
from functools import reduce as fold


ASSORTATIVITY_TITLE: str = "***ASSORTATIVITY***"
NEWLINES: str = "\n\n"


class CommunityData(NamedTuple):
    community_id: int
    average_age: float
    assortativity: float


class DegreeAssortativity:
    def __init__(self, ntwrk: nx.Graph):
        self.ntwrk = ntwrk
        self.community_data: List[CommunityData] = []
        self.overall_assortativity: float = nx.degree_assortativity_coefficient(ntwrk)
        comm_nodes: List[Tuple[str, int]] = sorted(list(dict(ntwrk.nodes(data=COMMUNITY, default=0)).items()),
                                                   key=lambda p: p[1])
        avg_age: float
        asst: float
        for comm, nodes in groupby(comm_nodes, key=lambda p: p[1]):
            nodes = list(map(lambda p: p[0], nodes))
            if len(nodes) == 0:
                continue
            age_dict = nx.get_node_attributes(ntwrk, INITIAL_AGE)
            avg_age = sum(map(lambda u: age_dict[u] if u in age_dict else 0, nodes))/len(nodes)
            asst = nx.degree_assortativity_coefficient(ntwrk, nodes=nodes)
            self.community_data.append(CommunityData(community_id=comm, average_age=avg_age, assortativity=asst))

    def __repr__(self) -> str:
        return f"Overall assortativity: {self.overall_assortativity}{NEWLINES}{fold(lambda v, acc: str(acc) + NEWLINES + str(v), self.community_data)}"


def assortativity_write_out(ntwrk: nx.Graph) -> str:
    return f"{ASSORTATIVITY_TITLE}\n{gen_assortativity(ntwrk)}"


def gen_assortativity(ntwrk: nx.Graph) -> DegreeAssortativity:
    return DegreeAssortativity(ntwrk)

