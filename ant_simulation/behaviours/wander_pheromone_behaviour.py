##############################
from __future__ import annotations
from typing import TYPE_CHECKING, Callable
##############################

if TYPE_CHECKING:
    from ant_simulation.actors.modular_ant import ModularAnt

from numpy import random, array
from ant_simulation.behaviours.direction_management import Direction, Directions
from architecture.world import World
from ant_simulation.behaviours.behaviour import Behaviour
from architecture.location import Location
from architecture.position import Position


########################################################################################################################
# The behaviour code.                                                                                                  #
########################################################################################################################
def pheromone_bias_func(bias: float) -> Callable[[World, Position, Direction, float], float]:
    def pheromone_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight + (bias * loc.get_pheromone_count() if loc.is_free() and weight != 0 else 0)
        except IndexError:
            return 0
    return pheromone_bias


def hold_direction_func(var_chance: float, prev_dir: Direction) -> Callable[[World, Position, Direction, float], float]:
    def hold_direction(_: World, __: Position, direction: Direction, weight: float) -> float:
        return weight if prev_dir.get() == direction.get() else var_chance * weight
    return hold_direction


class WanderPheromoneBehaviour(Behaviour):
    DEFAULT_VARIATION_CHANCE: float = 0.1
    DEFAULT_WOBBLE_CHANCE: float = 0.35


    def __init__(self, pheromone_bias: float = 0, variation_chance: float = DEFAULT_VARIATION_CHANCE,
                 wobble_chance: float = DEFAULT_WOBBLE_CHANCE):
        self.pheromone_bias: float = pheromone_bias
        self.variation_chance: float = variation_chance
        self.wobble_chance: float = wobble_chance
        self.facing: Direction = Direction(random.choice(array([-1, 0, -1])), random.choice(array([-1, 0, -1])))


    def update_attributes(self, pheromone_bias: float = None, variation_chance: float = None,
                 wobble_chance: float = None):
        self.pheromone_bias = pheromone_bias if pheromone_bias is not None else self.pheromone_bias
        self.variation_chance = variation_chance if variation_chance is not None else self.variation_chance
        self.wobble_chance = wobble_chance if wobble_chance is not None else self.wobble_chance


    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: ModularAnt):
        try:
            # Get a list of ALL possible directions to move in.
                # Compile list into a list of pairs, where the first entry is a direction, and the second a weight.
            directions: Directions = Directions(world, position)

            # Bias the direction in terms of the previous chosen direction.
            directions.bias(hold_direction_func(self.variation_chance, self.facing))

            # Bias the direction weights, by pheromone level (with respect to the bias amount).
            directions.bias(pheromone_bias_func(self.pheromone_bias))

            # Make a random, weighted selection of these direction.
            self.facing = directions.get_random_direction()

            # Apply a wobble at random.
            d: Direction = self.facing.get_wobble(random.choice(array([0, -1, 1]), p=array([1 - self.wobble_chance,
                                self.wobble_chance/2, self.wobble_chance/2])))
            to: Location = world.get_location(position.x + d.get()[0], position.y + d.get()[1])
            world.move(location, to)
        except IndexError:
            # The ant can't move...
            pass
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
