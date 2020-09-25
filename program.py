##############################
from __future__ import annotations
##############################
from ant_simulation.actors.modular_ant import ModularAnt
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.rendering.plotter import Plotter
from architecture.world import World


if __name__ == "__main__":
    registry.register()

    world: World = create_world("output.txt", "actors_lesser.txt", "empty.txt")
    for i in range(10):
        world.run(50)
        Plotter.draw_world(world)
    # TODO : Probably would want to export this data. Need a way of interpretting it and
    #  creating a network out of it.
    print(ModularAnt.interactions)
