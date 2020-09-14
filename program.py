##############################
from __future__ import annotations
##############################
from architecture.generation import registry
from architecture.generation.world_builder import create_world
from architecture.kinds import Kind
from architecture.rendering.plotter import Plotter
from architecture.world import World


if __name__ == "__main__":
    registry.register()

    world: World = create_world("output.txt", "actors_random_walks.txt", "objects.txt")
    for i in range(10):
        world.run(500)
        Plotter.draw_world(world, Kind.FOOD)
