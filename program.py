##############################
from __future__ import annotations
##############################
import random
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
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.plotter import Plotter
from architecture.world import World
from architecture.exceptions.invalid_char import InvalidCharacterException


if __name__ == "__main__":
    file_name = "output.txt"

    file = open(file_name, "r")
    width = 0
    height = 0
    for line in file:
        if height == 0:
            width = len(line.split())
        height += 1
    file.close()
    this_World = World(width,height)

    factory.register_ground(Tunnel.get_id(), Tunnel.create)
    factory.register_ground(Nest.get_id(), Nest.create)
    factory.register_ground(ForageGrounds.get_id(), ForageGrounds.create)
    factory.register_ground(Wall.get_id(), Wall.create)

    file = open(file_name, "r")
    line_no = 0
    for line in file:
        line_list = line.split()
        for i in range(len(line_list)):
            #forage_key = 'f'
            #nest_key = 'n'
            #tunnel_key = 't'
            #wall_key = "w"
            if line_list[i] == "t" :
                this_World.set_location(Location(factory.make_ground("Tunnel", Position(i,line_no))),i,line_no)
            elif line_list[i] == "n":
                this_World.set_location(Location(factory.make_ground("Nest", Position(i,line_no))),i,line_no)
            elif line_list[i] == "f":
                this_World.set_location(Location(factory.make_ground("ForageGrounds", Position(i,line_no))),i,line_no)
            elif line_list[i] == "w":
                this_World.set_location(Location(factory.make_ground("Wall", Position(i,line_no))),i,line_no)
            else:
                raise InvalidCharacterException()

        line_no += 1

    file.close()

    # TODO :
    #   -> Create a file-reader which accepts a file such as is output by txt_creator.py and
    #      uses the factory to generate the relevant Objects, Actors and Grounds.
    #       => Actors and Objects will need to be listed, rather than provided in a grid, since
    #          they have a series of Kinds, and also are not present necessarily in every Location.
    #   -> Populate a World with these.


    factory.register_actor(Ant.get_id(), Ant.create)
    factory.register_actor(Nurse.get_id(), Nurse.create)
    factory.register_actor(Forager.get_id(), Forager.create)
    factory.register_actor(Queen.get_id(), Queen.create)
    factory.register_actor(Cleaner.get_id(), Cleaner.create)

    # Access the private dictionary for the Kind enum to get the kind by its string name.
    #actor: Actor = factory.make_actor("ant", Position(2,2), Kind["DEFAULT"])
    #print("Here's a factory-generated ant:")
    #print(actor.get_id())
    #print("Here are the Kinds attached to this ant:")
    #print(actor.get_kinds())
    #make_and_show_box()

    list_of_ants_to_insert = ["Forager"] * 3 + ["Nurse"] * 5 + ["Cleaner"] * 3 + ["Queen"] * 1
    while len(list_of_ants_to_insert) > 0:
        y = random.randrange(0, height)
        x = random.randrange(0, width)
        if this_World.get_location(x, y).is_free():
            this_World.get_location(x, y).set_actor(factory.make_actor(list_of_ants_to_insert[-1]))
            list_of_ants_to_insert.pop()
    Plotter.draw_world(this_World)
