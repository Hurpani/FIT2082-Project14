##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

if TYPE_CHECKING:
    from deprecated.behaviour_ant import BehaviourAnt
    from architecture.actor import Actor

from ant_simulation.behaviours.behaviour import Behaviour
from architecture.location import Location
from architecture.position import Position
from architecture.world import World
from architecture.rendering.colour import Colour
import random


class WanderBehaviour(Behaviour):
    DEFAULT_VARIATION_CHANCE: float = 0.1
    DEFAULT_WOBBLE_CHANCE: float = 0.35

    @staticmethod
    def move(actor: Actor, frm: Location, to: Location):
        to.set_actor(actor)
        frm.remove_actor()


    # TODO : Implement pheromone biasing.
    def __init__(self, pheromone_bias: float = 0, variation_chance: float = DEFAULT_VARIATION_CHANCE,
                 wobble_chance: float = DEFAULT_WOBBLE_CHANCE):
        self.variation_chance: float = variation_chance
        self.wobble_chance: float = wobble_chance
        self.pheromone_bias: float = pheromone_bias


    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: BehaviourAnt):
        try:
            # COMPLETELY RANDOM CHOICES FOR WALKS (no preserving of direction).
            # to: Location = Random().choice(world.get_adjacent_locations(position.x, position.y, 1, True))
            # WanderBehaviour.move(ant, location, to)
            self.change_dir_random_chance(world, elapsed, location, position, self.variation_chance, self.wobble_chance,
                                          ant)
        except IndexError:
            # The ant can't find anywhere to move...
            pass


    def get_colour(self) -> Colour:
        return Colour()


    def tick(self, world: World, elapsed: float, location: Location, pos: Position):
        self.do(world, elapsed, location, pos, self)


    def change_dir_random_chance(self, world: World, elapsed: float, location: Location, pos: Position,
                                 variation_chance: float, wobble_chance: float, ant: BehaviourAnt):
        def give_dir_next_to_current(i, j):
            if i == -1 and j == 1:
                if random.random() > 0.5:
                    return ([[-1, 0], [0, 1]])
                return ([[0, 1], [-1, 0]])
            if i == -1 and j == 0:
                if random.random() > 0.5:
                    return ([[-1, 1], [-1, -1]])
                return ([[-1, -1], [-1, 1]])
            if i == -1 and j == -1:
                if random.random() > 0.5:
                    return ([[-1, 0], [0, -1]])
                return ([[0, -1], [-1, 0]])
            if i == 0 and j == 1:
                if random.random() > 0.5:
                    return ([[-1, 1], [1, 1]])
                return ([[1, 1], [-1, 1]])
            if i == 0 and j == -1:
                if random.random() > 0.5:
                    return ([[-1, -1], [1, -1]])
                return ([[1, -1], [-1, -1]])
            if i == 1 and j == 1:
                if random.random() > 0.5:
                    return ([[0, 1], [1, 0]])
                return ([[1, 0], [0, 1]])
            if i == 1 and j == 0:
                if random.random() > 0.5:
                    return ([[1, 1], [1, -1]])
                return ([[1, -1], [1, 1]])
            if i == 1 and j == -1:
                if random.random() > 0.5:
                    return ([[1, 0], [0, -1]])
                return ([[0, -1], [1, 0]])


        def change_dir_random(world: World, elapsed: float, location: Location, pos: Position):
            possible_free_locations = []
            # scan 1 range saving taking note of all available spots
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i != 0 and j != 0:
                        if world.get_location(pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j).is_free():
                            possible_free_locations.append(
                                [pos.get_coordinates()[0] + i, pos.get_coordinates()[1] + j, i, j])
            # if at least 1 available spot in 1 range
            if len(possible_free_locations) > 0:
                # pick a random one and move there
                random_available_space = random.choice(possible_free_locations)
                WanderBehaviour.move(ant, world.get_location(pos.x, pos.y),
                                     world.get_location(random_available_space[0], random_available_space[1]))
                ant.current_dir = [random_available_space[2], random_available_space[3]]


        if variation_chance < random.random():  # 90% of the time
            # if spot in same direction is free and passes a 33% chance, go there
            if world.get_location(pos.get_coordinates()[0] + ant.current_dir[0],
                                  pos.get_coordinates()[1] + ant.current_dir[
                                      1]).is_free() and random.random() < wobble_chance:
                WanderBehaviour.move(ant, world.get_location(pos.x, pos.y),
                                     world.get_location(pos.get_coordinates()[0] + ant.current_dir[0],
                                                        pos.get_coordinates()[1] + ant.current_dir[1]))
            else:
                # with a 50% choose the adjacent spot e.g. if going north, pick north-east 50% of the time , north-west 50% of the time
                next_dirr = give_dir_next_to_current(ant.current_dir[0], ant.current_dir[1])

                # if the first picked adjacent spot is free go there
                if world.get_location(pos.get_coordinates()[0] + next_dirr[0][0],
                                      pos.get_coordinates()[1] + next_dirr[0][1]).is_free():
                    WanderBehaviour.move(ant, world.get_location(pos.x, pos.y),
                                         world.get_location(pos.get_coordinates()[0] + next_dirr[0][0],
                                                            pos.get_coordinates()[1] + next_dirr[0][1]))

                # else if the second picked adjacent spot is free go there
                elif world.get_location(pos.get_coordinates()[0] + next_dirr[1][0],
                                        pos.get_coordinates()[1] + next_dirr[1][1]).is_free():
                    WanderBehaviour.move(ant, world.get_location(pos.x, pos.y),
                                         world.get_location(pos.get_coordinates()[0] + next_dirr[1][0],
                                                            pos.get_coordinates()[1] + next_dirr[1][1]))

                # else go random available spot ... and if no spot available change_dir_random will make the ant stay still
                else:
                    change_dir_random(world, elapsed, location, pos)

        else:  # 10% of the time go random available spot ... and if no spot available change_dir_random will make the ant stay still
            change_dir_random(world, elapsed, location, pos)
