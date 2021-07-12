##############################
from __future__ import annotations
##############################
from ant_simulation.analysis.automated_testing import batch_test
from ant_simulation.analysis.analyse import analyse_in
# import networkx as nx
# from ant_simulation.analysis.graph_analysis import display_network


def perform_testing() -> None:
    # Example batch:
    batch_test("tests", 1, [("output.txt", "actors.txt", "world_objects.txt", 86400)],
               [{"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 1},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 2},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 3},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 4},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 5}])


def perform_analysis() -> None:
    analyse_in("./network_outputs/tests/", "./network_outputs/analyses")


if __name__ == "__main__":
    # display_network(nx.read_graphml("./network_outputs/demo_test/network_0-1(2).gml"))

    perform_testing()
    perform_analysis()

    print("Hello, World! (todo: request command-line inputs from a user)")

