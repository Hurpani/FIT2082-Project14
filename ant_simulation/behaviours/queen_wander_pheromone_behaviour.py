##############################
from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Union

##############################
from ant_simulation.behaviours.wander_pheromone_behaviour import WanderPheromoneBehaviour, hold_direction_func, \
    pheromone_bias_func, brood_pheromone_bias_func, age_bias

if TYPE_CHECKING:
    from ant_simulation.actors.modular_ant import ModularAnt

from numpy import random, array, exp
from ant_simulation.behaviours.direction_management import Direction, Directions
from architecture.world import World
from architecture.location import Location
from architecture.position import Position


########################################################################################################################
# The behaviour code.                                                                                                  #
########################################################################################################################
def brood_direction_func(holdness: float, brood_pos: (int, int)) -> Callable[[World, Position, Direction, float], float]:
    def brood_direction(_: World, pos: Position, direction: Direction, weight: float) -> float:
        return Direction.similarity_score(Direction(brood_pos[0] - pos.x, brood_pos[1] - pos.y), direction) * \
               holdness * weight
        # return weight if prev_dir.get() != direction.get() else holdness * weight
    return brood_direction

class QueenWanderPheromoneBehaviour(WanderPheromoneBehaviour):
    DEFAULT_VARIATION_CHANCE: float = 0.1
    DEFAULT_WOBBLE_CHANCE: float = 0.35


    def __init__(self, pheromone_bias: float = 0, hold_chance: float = DEFAULT_VARIATION_CHANCE,
                 wobble_chance: float = DEFAULT_WOBBLE_CHANCE):
        self.brood_position: Union[(int, int), None] = None
        super().__init__(pheromone_bias, hold_chance, wobble_chance)


    def set_brood_position(self, p: (int, int)):
        self.brood_position = p


    def do(self, world: World, elapsed: float, location: Location, position: Position, ant: ModularAnt):
        try:
            # Get a list of ALL possible directions to move in.
                # Compile list into a list of pairs, where the first entry is a direction, and the second a weight.
            directions: Directions = Directions(world, position)

            # Bias the direction in terms of the origin position.
            if self.brood_position is not None:
                directions.bias(brood_direction_func(self.hold_chance, self.brood_position))

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
