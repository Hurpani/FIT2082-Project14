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

if __name__ == "__main__":
    registry.register()

    # # The old way.
    # world: World = create_world("output.txt", "actors.txt", "world_objects.txt")
    # for i in range(20):
    #     world.run(1000)
    #     Plotter.draw_world(world)

    # Continue from where we left off.
    world: World = load("output.txt", "world_save.txt", "world_objects.txt")
    for i in range(20):
        world.run(10000)
        save(world)
        Plotter.draw_world(world)#, Kind.BROOD)
    export_data_to_edge_list_file(ModularAnt.interactions)
    create_and_view_networkx("edge_list.txt", 210)