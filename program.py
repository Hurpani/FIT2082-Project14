##############################
from __future__ import annotations
##############################
from ant_simulation.analysis.automated_testing import batch_test
from ant_simulation.analysis.analyse import analyse_in


def perform_testing() -> None:
    # Example batch:
    batch_test("demo_test", 2, [("output.txt", "actors.txt", "world_objects.txt", 500)],
               [{"testing_scale": 1.0, "pheromone_testing_scale": 1.0, "interacting_ticks_threshold": 3},
                {"testing_scale": 10.0, "pheromone_testing_scale": 2.0, "interacting_ticks_threshold": 3}])


def perform_analysis() -> None:
    analyse_in("./network_outputs/demo_test/", "./network_outputs/demo_analyses")


if __name__ == "__main__":
    print("Hello, World! (todo: request command-line inputs from a user)")

