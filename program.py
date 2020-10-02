##############################
from __future__ import annotations
##############################
from ant_simulation.actors.modular_ant import ModularAnt
from ant_simulation.network_processing import create_and_view_networkx, export_data_to_edge_list_file
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.rendering.plotter import Plotter
from architecture.world import World

if __name__ == "__main__":
    registry.register()

    world: World = create_world("output.txt", "actors.txt", "empty.txt")
    # # # These two lines would restore a world from a previous run. # # #
    # world: World = create_world("output.txt", "saves/world_save.txt")
    # world.restore_pheromones()
    for i in range(20):
        world.run(1000)
        world.write_out()
        Plotter.draw_world(world)
    #export_data_to_edge_list_file(ModularAnt.interactions)
    #create_and_view_networkx("edge_list.txt", 0)