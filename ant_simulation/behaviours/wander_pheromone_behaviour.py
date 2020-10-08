##############################
from __future__ import annotations
from typing import TYPE_CHECKING, Callable
##############################

if TYPE_CHECKING:
    from ant_simulation.actors.modular_ant import ModularAnt

from numpy import random, array, exp
from ant_simulation.behaviours.direction_management import Direction, Directions
from architecture.world import World
from ant_simulation.behaviours.behaviour import Behaviour
from architecture.location import Location
from architecture.position import Position


def age_bias(bias: float, age: float) -> float:
    """\
Pheromone biasing decays at a rate corresponding to an inverse exponential
    function.
    """
    AGE_SCALE: float = 50
    return exp(-1 * age/AGE_SCALE) * bias


########################################################################################################################
# The behaviour code.                                                                                                  #
########################################################################################################################
def brood_pheromone_bias_func(age: float) -> Callable[[World, Position, Direction, float], float]:
    def brood_bias(age: float) -> float:
        #A, B, C, D, E = 3, 1.65, 0.07, -4.8, 2.33  # yields a function which decays quickly around the mean cleaner age.
        #return (A + B*(age - D)/E)*exp(-C*(age - D)/E)
        if age < 160:
            return (3 + 1.65 * (age + 4.8) / 2.33) * exp(-0.07 * (age + 4.8) / 2.33)
        return 0

    def brood_pheromone_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight + (brood_bias(age) * loc.get_pheromone_count() if loc.is_free() and weight != 0 else 0)
        except IndexError:
            return 0
    return brood_pheromone_bias

def pheromone_bias_func(bias: float) -> Callable[[World, Position, Direction, float], float]:
    def pheromone_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight + (bias * loc.get_pheromone_count() if loc.is_free() and weight != 0 else 0)
        except IndexError:
            return 0
    return pheromone_bias


def hold_direction_func(holdness: float, prev_dir: Direction) -> Callable[[World, Position, Direction, float], float]:
    def hold_direction(_: World, __: Position, direction: Direction, weight: float) -> float:
        return Direction.similarity_score(prev_dir, direction) * holdness * weight
        # return weight if prev_dir.get() != direction.get() else holdness * weight
    return hold_direction


class WanderPheromoneBehaviour(Behaviour):
    DEFAULT_VARIATION_CHANCE: float = 0.1
    DEFAULT_WOBBLE_CHANCE: float = 0.35


    def __init__(self, pheromone_bias: float = 0, hold_chance: float = DEFAULT_VARIATION_CHANCE,
                 wobble_chance: float = DEFAULT_WOBBLE_CHANCE):
        self.pheromone_bias: float = pheromone_bias
        self.hold_chance: float = hold_chance
        self.wobble_chance: float = wobble_chance
        self.facing: Direction = Direction(random.choice(array([-1, 0, -1])), random.choice(array([-1, 0, -1])))
        self.age: float = 0


    def set_age(self, _age: float):
        self.age = _age


    def update_attributes(self, pheromone_bias: float = None, variation_chance: float = None,
                 wobble_chance: float = None):
        self.pheromone_bias = pheromone_bias if pheromone_bias is not None else self.pheromone_bias
        self.hold_chance = variation_chance if variation_chance is not None else self.hold_chance
        self.wobble_chance = wobble_chance if wobble_chance is not None else self.wobble_chance


    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: ModularAnt):
        try:
            # Get a list of ALL possible directions to move in.
                # Compile list into a list of pairs, where the first entry is a direction, and the second a weight.
            directions: Directions = Directions(world, position)

            # Bias the direction in terms of the previous chosen direction.
            directions.bias(hold_direction_func(self.hold_chance, self.facing))

            # Bias the direction weights, by pheromone level (with respect to the bias amount).
            directions.bias(pheromone_bias_func(age_bias(self.pheromone_bias, self.age)))

            # Bias by brood pheromones, encouraging ants to adopt a nurse role.
            directions.bias(brood_pheromone_bias_func(self.age))

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
