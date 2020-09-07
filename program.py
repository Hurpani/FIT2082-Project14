##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################
import random
import networkx as nx
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors
from ant_simulation.ant import Ant,Foarager,Cleaner,Queen,Nurse
from architecture.actor import Actor
from architecture.generation import factory
from architecture.ground import Tunnel,Nest,ForageGrounds,Wall
from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.plotter import Plotter
from architecture.world import World
from architecture.exceptions.invalid_char import InvalidCharacterException
def make_and_show_box():
    # average non queen is 16mm long with a range of 9.7mm to 26.3mm
    # given a 16mm^2 grid the boxes are 160mm * 256mm

    box_nest = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    ]

    box_foraging_arena = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    box_tunnel = [
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    stiched_map = []

    for i in range(len(box_nest)):
        stiched_map.append(box_foraging_arena[i] + box_nest[i])
    for i in range(len(box_tunnel)):
        stiched_map.append(box_tunnel[i])

    cmap = mpl.colors.ListedColormap([(1,1,0,1), 'Black'])
    plt.figure(figsize=(len(stiched_map[0]), len(stiched_map)))
    plt.pcolor(stiched_map[::-1], cmap=cmap, edgecolors='k', linewidths=1)
    for l in stiched_map:
        print(l)
    plt.show()


if __name__ == "__main__":
    file_name = "output.txt"

    file = open(file_name,"r")
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
                this_World.set_location(factory.make_ground("Tunnel", Position(i,line_no)),i,line_no)
            elif line_list[i] == "n":
                this_World.set_location(factory.make_ground("Nest", Position(i,line_no)),i,line_no)
            elif line_list[i] == "f":
                this_World.set_location(factory.make_ground("ForageGrounds", Position(i,line_no)),i,line_no)
            elif line_list[i] == "w":
                this_World.set_location(factory.make_ground("Wall", Position(i,line_no)),i,line_no)
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
    factory.register_actor(Foarager.get_id(), Foarager.create)
    factory.register_actor(Queen.get_id(), Queen.create)
    factory.register_actor(Cleaner.get_id(), Cleaner.create)

    # Access the private dictionary for the Kind enum to get the kind by its string name.
    #actor: Actor = factory.make_actor("ant", Position(2,2), Kind["DEFAULT"])
    #print("Here's a factory-generated ant:")
    #print(actor.get_id())
    #print("Here are the Kinds attached to this ant:")
    #print(actor.get_kinds())
    #make_and_show_box()

    list_of_ants_to_insert = ["Forager"] * 39 + ["Nurse"] * 67 + ["Cleaner"] * 44 + ["Queen"] * 1
    while len(list_of_ants_to_insert) > 0:
        y = random.randrange(0, height)
        x = random.randrange(0, width)
        if this_World.world[y][x].is_free and type(this_World.world[y][x]) == Nest:
            this_World.set_location(factory.make_actor(list_of_ants_to_insert[-1], Position(x, y)), x, y)
            list_of_ants_to_insert.pop()
    Plotter.draw_world(this_World)
