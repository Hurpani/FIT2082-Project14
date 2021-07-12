from typing import List
import networkx as nx
from ant_simulation.analysis.metrics import analyse_assortativity
from pathlib import Path
from glob import glob


FORMAT: str = "*.gml"
SUFFIX: str = "_analysis.txt"


def analysis_of(ntwrk: nx.Graph) -> str:
    return analyse_assortativity.assortativity_write_out(ntwrk)


def analyse_in(read_from_path: str, write_to_path: str) -> None:
    network_paths: List[Path] = list(map(Path, glob(read_from_path + FORMAT, recursive=False)))
    ntwrk: nx.Graph
    name: str
    for path in network_paths:
        name = path.name + SUFFIX
        ntwrk = nx.read_graphml(path)
        with (Path(write_to_path) / Path(name)).open('w') as file:
            file.write(analysis_of(ntwrk))


