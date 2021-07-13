##############################
from __future__ import annotations
##############################
from ant_simulation.analysis.automated_testing import batch_test
from ant_simulation.analysis.analyse import analyse_in
# import networkx as nx
# from ant_simulation.analysis.graph_analysis import display_network


def perform_testing() -> None:
    # Example batch:
                                                    # 86,400 / 16 (so expecting 60,000 -> 3,750 for 1 tick delay)
    batch_test("interaction_count_calib_folder", 1, [("output.txt", "actors.txt", "world_objects.txt", 5400)],
               [
                # {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 1},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 2},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 3},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 4},
                {"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 5}
               ])


def perform_analysis() -> None:
    analyse_in("./network_outputs/interaction_count_calib_folder/",
               "./network_outputs/analyses_interaction_count_calib_folder")


if __name__ == "__main__":
    # display_network(nx.read_graphml("./network_outputs/demo_test/network_0-1(2).gml"))
    # FIXME: Perhaps limit the maximum number of brood pheromones (further?) - the nurses
    #  are clumping like heck. Also seemed like directly using values of A,B,C,D,E in
    #  brood bias factor caused issues?

    perform_testing()
    perform_analysis()

    print("Hello, World! (todo: request command-line inputs from a user)")

