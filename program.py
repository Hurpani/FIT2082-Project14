##############################
from __future__ import annotations
##############################
from ant_simulation.analysis.automated_testing import batch_test
# from ant_simulation.analysis.metrics.analyse_simrank import gen_simrank
# import networkx as nx

if __name__ == "__main__":
    batch_test("demo_test", 2, [("output.txt", "actors.txt", "world_objects.txt", 500)],
               [{"testing_scale": 1.0, "pheromone_testing_scale": 1.0},
                {"testing_scale": 10.0, "pheromone_testing_scale": 2.0}])
    # print(gen_simrank(nx.read_graphml("./network_outputs/demo_test/network_0-0(1).gml")))

