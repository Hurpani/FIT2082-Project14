##############################
from __future__ import annotations
##############################
from typing import List, Tuple, Dict
from ant_simulation.actors.modular_ant import ModularAnt
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.world import World
from ant_simulation.analysis import graph_analysis
import networkx as nx
from pathlib import Path

PARENT_DIRECTORY: str = "network_outputs"
FILE_PREFIX: str = "network"
DESC_FILE_PREFIX: str = "arguments"
# The maximum density of an interaction network; this is a
# constant, as fixed/specified in the paper by Mersch, et al (2013).
NETWORK_DENSITY: float = 0.25
# We fix a maximum community count; this number minus one gives the
# number of communities considered genuine (the largest of these
# survive) whilst the remainder are merged.
#
# For the case of 3, we have at most 2 main communities, and the
# remainder merged. Communities are identified using the Infomap
# community-finding algorithm.
MAX_COMMUNITIES: int = 3


def file_suffix(k: int, p: int, r: int) -> str:
    return f"{FILE_PREFIX}_{k}-{p}({r}).gml"


def desc_file_suffix(k: int, p: int) -> str:
    return f"{DESC_FILE_PREFIX}_{k}-{p}.txt"


def batch_test(folder: str, runs: int,
               base_seq: List[Tuple[str, str, str, int]],
               arguments: List[Dict[str, float]]) -> None:
    """\
The folder argument should specify a folder for the sequence of outputs of
    each run to be written in. This will be nested within ./network_outputs/.

    The runs argument determines how many times each particular configuration should
    be run.

    The base_seq argument should be a list of quadruples of ground, actor and object
    files, followed by simulation lengths which you want tested in each combination
    of arguments given by the arguments argument.
    """
    registry.register()

    pth: Path = Path(f"{Path.cwd()}/{PARENT_DIRECTORY}/{folder}/")
    dsc_pth: Path
    ntw_pth: Path
    ntwrk: nx.Graph
    n: int
    m: int

    if not pth.exists():
        pth.mkdir()
    n = len(base_seq)
    m = max(1, len(arguments))
    print("Working...")
    for i in range(n):
        for j in range(m):
            dsc_pth = pth / desc_file_suffix(i, j)
            with dsc_pth.open('w') as file:
                file.write(f"[Base: {base_seq[i]}]\n")
                for k, v in arguments[j].items():
                    file.write(f"{k}: {v}\n")
            for run in range(runs):
                print(f"\nTesting {base_seq[i][3]} ticks with arguments: {arguments[j]}")
                ntw_pth = pth / file_suffix(i, j, run + 1)
                ntwrk = run_test(*base_seq[i], **arguments[j])
                nx.write_graphml(ntwrk, ntw_pth)
                print(f"Completed test {i}-{j}, run {run + 1}/{runs}.")
    print("Testing complete!")


def run_test(grd: str, act: str, obj: str, run_time: int, **kwargs) -> nx.Graph:
    ModularAnt.wipe_interactions()
    world: World = create_world(grd, act, obj, **kwargs)
    world.run(run_time)
    ntwrk, _ = graph_analysis.find_communities(
        graph_analysis.construct_network(
            ModularAnt.get_interactions(), NETWORK_DENSITY, ModularAnt.get_initial_ages()
        ), MAX_COMMUNITIES, False
    )
    return ntwrk



