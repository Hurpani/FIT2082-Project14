##############################
from __future__ import annotations

from typing import TYPE_CHECKING, Callable
##############################
from ant_simulation.grounds.forage_grounds import ForageGrounds
from architecture.kinds import Kind

if TYPE_CHECKING:
    from ant_simulation.actors.modular_ant import ModularAnt
from numpy import random, array, exp, tanh
from ant_simulation.behaviours.direction_management import Direction, Directions, sign
from architecture.world import World
from ant_simulation.behaviours.behaviour import Behaviour
from architecture.location import Location
from architecture.position import Position

FORAGING_PHEROMONE_THRESHOLD: int = 3
FOOD_LURE_RADIUS: int = 5
FORAGING_AGE: int = 130
FOOD_BIAS_FACTOR: int = 15


def age_bias(bias: float, age: float) -> float:
    """\
Pheromone biasing decays at a rate corresponding to an inverse exponential
    function.
    """
    AGE_SCALE: float = 50
    return exp(-1 * age / AGE_SCALE) * bias


def zero_inv_mult(a: float, b: float) -> float:
    """\
Multiplication under this function treats pre-multiplication by zero as a universal multiplicative inverse.
This is useful for not scaling weightings when the testing scale is zero.
    """
    return 1 if a == 0 else a * b


########################################################################################################################
# The behaviour code.                                                                                                  #
########################################################################################################################
def brood_pheromone_bias_func(age: float) -> Callable[[World, Position, Direction, float], float]:
    def brood_bias(age: float) -> float:
        # A, B, C, D, E = 3, 1.65, 0.07, -4.8, 2.33  # yields a function which decays quickly around the mean cleaner age.
        # return (A + B*(age - D)/E)*exp(-C*(age - D)/E)
        if age < 160:
            return (3 + 1.65 * (age + 4.8) / 2.33) * exp(-0.07 * (age + 4.8) / 2.33)
        return 0

    def brood_pheromone_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight + (
                    world.get_pheromone_testing_scale() *
                    (brood_bias(age) * loc.get_pheromone_count() if loc.is_free() and weight != 0 else 0)
            )
        except IndexError:
            return 0

    return brood_pheromone_bias


def pheromone_bias_func(bias: float) -> Callable[[World, Position, Direction, float], float]:
    def pheromone_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight + (
                    world.get_pheromone_testing_scale() *
                    (bias * loc.get_pheromone_count() if loc.is_free() and weight != 0 else 0)
            )
        except IndexError:
            return 0

    return pheromone_bias


def hold_direction_func(holdness: float, prev_dir: Direction) -> Callable[[World, Position, Direction, float], float]:
    def hold_direction(world: World, __: Position, direction: Direction, weight: float) -> float:
        return zero_inv_mult(
            world.get_testing_scale(),
            Direction.clamped_similarity(prev_dir, direction) * holdness * weight
        )

    return hold_direction


def exploration_bias_func(age: float) -> Callable[[World, Position, Direction, float], float]:
    def exploration_bias(world: World, position: Position, direction: Direction, weight: float) -> float:
        try:
            loc: Location = world.get_location(position.x + direction.get()[0], position.y + direction.get()[1])
            return weight * (
                    world.get_pheromone_testing_scale() *
                    (
                        (tanh((age - 130) / 10) + 2)
                        if ((loc.get_pheromone_count() <= FORAGING_PHEROMONE_THRESHOLD and
                             loc.get_brood_pheromone_count() <= FORAGING_PHEROMONE_THRESHOLD) or
                            loc.get_foraging_pheromone_count() > FORAGING_PHEROMONE_THRESHOLD)
                        else weight
                    )
            )
        except IndexError:
            return 0

    return exploration_bias


def id_func() -> Callable[[World, Position, Direction, float], float]:
    """\
The id_func function returns a map which does not alter a weight.
    """

    def id_f(world: World, position: Position, direction: Direction, weight: float) -> float:
        return weight

    return id_f


def food_lure_func(age: float) -> Callable[[World, Position, Direction, float], float]:
    """\
Ants of sufficient age will be enticed by food outside of the nest, whilst ants pick up food, and place
    it near piles inside of the nest.
    """

    def food_lure(world: World, position: Position, direction: Direction, weight: float) -> float:
        locations: [(Location, int, int)] = world.get_adjacent_locations_with_positions(position.x, position.y,
                                                                                        FOOD_LURE_RADIUS, True)
        return weight + world.get_testing_scale() * sum(
            map(lambda lxy: FOOD_BIAS_FACTOR * len(lxy[0].get_objects(Kind.FOOD)),
                filter(lambda lxy: (sign(lxy[1] - position.x) == sign(direction.x) or direction.x == 0) and (
                        sign(lxy[2] - position.y) == sign(direction.y) or direction.y == 0),
                       filter(lambda lxy: lxy[0].get_ground().get_id() == ForageGrounds.get_id(),
                              locations)
                       )
                )
        )

    return food_lure if age > FORAGING_AGE else id_func()


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
        self.seeking_food: bool = False

    def set_age(self, _age: float):
        self.age = _age

    def set_seeking_food(self, _seeking_food: bool):
        self.seeking_food = _seeking_food

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

            directions.bias_seq(
                # Bias the direction in terms of the previous chosen direction.
                hold_direction_func(self.hold_chance, self.facing),
                # Bias the direction weights, by pheromone level (with respect to the bias amount).
                pheromone_bias_func(age_bias(self.pheromone_bias, self.age)),
                # Bias by brood pheromones, encouraging ants to adopt a nurse role.
                brood_pheromone_bias_func(self.age),
                # Bias by forager pheromones, and against other pheromones based on age.
                exploration_bias_func(self.age),
                # Bias by food in the foraging area, if the ant is not already carrying food.
                food_lure_func(self.age) if self.seeking_food else id_func()
            )

            # Make a random, weighted selection of these directions.
            self.facing = directions.get_random_direction()

            # Apply a wobble at random.
            d: Direction = self.facing.get_wobble(random.choice(array([0, -1, 1]), p=array([1 - self.wobble_chance,
                                                                                            self.wobble_chance / 2,
                                                                                            self.wobble_chance / 2])))
            to: Location = world.get_location(position.x + d.get()[0], position.y + d.get()[1])
            world.move(location, to)
        except IndexError:
            # The ant can't move...
            pass
########################################################################################################################
#                                                                                                                      #
########################################################################################################################
