##############################
from __future__ import annotations
##############################
from ant_simulation.actors.modular_ant import ModularAnt
from ant_simulation.network_processing import create_and_view_networkx, export_data_to_edge_list_file
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.kinds import Kind
from architecture.rendering.plotter import Plotter
from architecture.saver import save, load
from architecture.world import World
from ant_simulation.analysis import graph_analysis

if __name__ == "__main__":
    registry.register()
    world: World = create_world("output.txt", "actors.txt", "world_objects.txt", 10.0, 5.0)
    world.run(20000)
    Plotter.draw_world(world)
    save(world)
    export_data_to_edge_list_file(ModularAnt.interactions)
    graph_analysis.display_network(
        *graph_analysis.find_communities(
            graph_analysis.gen_light_network("edge_list.txt", 0.25)
        )
    )


    # for i in range(20):
    #     world.run(1000)
    #     Plotter.draw_world(world)

    # Continue from where we left off.
    # world: World = load("output.txt", "world_save.txt", "world_objects.txt")
    # for i in range(75):
    #     world.run(100)
    #     Plotter.draw_world(world)  # , Kind.BROOD)
    #     save(world)
    # print(sum(ModularAnt.interactions.values()))
    # export_data_to_edge_list_file(ModularAnt.interactions)
    # create_and_view_networkx("edge_list.txt", 15)  # 210 # 210*3
