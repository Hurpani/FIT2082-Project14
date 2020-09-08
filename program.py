##############################
from __future__ import annotations
##############################
from ant_simulation.actors.ant import Ant
from ant_simulation.actors.cleaner import Cleaner
from ant_simulation.actors.forager import Forager
from ant_simulation.actors.nurse import Nurse
from ant_simulation.actors.queen import Queen
from ant_simulation.grounds.forage_grounds import ForageGrounds
from ant_simulation.grounds.nest import Nest
from ant_simulation.grounds.tunnel import Tunnel
from ant_simulation.grounds.wall import Wall
from architecture.generation import factory
from architecture.generation.world_builder import create_world
from architecture.rendering.plotter import Plotter
from architecture.world import World


if __name__ == "__main__":
    factory.register_actor(Ant.get_id(), Ant.create)
    factory.register_actor(Nurse.get_id(), Nurse.create)
    factory.register_actor(Forager.get_id(), Forager.create)
    factory.register_actor(Queen.get_id(), Queen.create)
    factory.register_actor(Cleaner.get_id(), Cleaner.create)

    factory.register_ground(Tunnel.get_id(), Tunnel.create)
    factory.register_ground(Nest.get_id(), Nest.create)
    factory.register_ground(ForageGrounds.get_id(), ForageGrounds.create)
    factory.register_ground(Wall.get_id(), Wall.create)

    world: World = create_world("output.txt", "actors.txt", "")
    world.run(5)
    Plotter.draw_world(world)
