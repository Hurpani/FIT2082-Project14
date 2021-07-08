##############################
from __future__ import annotations
##############################
from ant_simulation.analysis.automated_testing import batch_test

if __name__ == "__main__":
    batch_test("demo_test", [("output.txt", "actors.txt", "world_objects.txt", 1000)],
               [{"testing_scale": 1.0, "pheromone_testing_scale": 1.0},
                {"testing_scale": 10.0, "pheromone_testing_scale": 2.0}])

