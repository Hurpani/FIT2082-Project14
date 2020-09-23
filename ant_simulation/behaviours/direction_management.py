##############################
from __future__ import annotations
from typing import Callable
##############################
from architecture.exceptions.invalid_location import InvalidLocationException

from numpy import random, array
from architecture.world import World
from architecture.location import Location
from architecture.position import Position

# FIXME: Wobbling seems to allow for the ant to move through 1-thick walls... seems like the rotation needs to be
#  rounded-off better.

########################################################################################################################
# These functions and classes are concerned with managing directions.
########################################################################################################################
def sign(n: int) -> int:
    return 1 if n > 0 else (-1 if n < 0 else 0)


class Direction:

    def __init__(self, x: int, y: int):
        """\
    x, y in {-1, 0, 1}.
        """
        self.x = sign(x)
        self.y = sign(y)

    def get_wobble(self, dir: int):
        """\
    Returns a direction, rotated 45 degrees, clockwise if dir is negative,
        anticlockwise if dir is positive, or not rotated if dir is zero.
        """
        return Direction(
            sign(self.x - sign(dir) * self.y),
            sign(self.x * sign(dir) + self.y)
        )

    def get(self) -> (int, int):
        return self.x, self.y


class Directions:
    """\
The Directions class manages pairs of possible movement directions, and associated
    weights.
    """

    def __init__(self, world: World, position: Position):
        self.world: World = world
        self.position: Position = position
        self.directions: [(Direction, float)] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j:
                    continue
                weight: float
                try:
                    loc: Location = world.get_location(position.x + i, position.y + j)
                    weight = 1 if loc.is_free() else 0
                except (IndexError, InvalidLocationException):
                    weight = 0
                self.directions.append((Direction(i, j), weight))


    def bias(self, func: Callable[[World, Position, Direction, float], float]):
        """\
    Accepts a function which maps a World, Position, Direction, and current weight to a new weight. Uses
        this function change the weightings associated with each direction.
        """
        for i in range(len(self.directions)):
            self.directions[i] = (self.directions[i][0],
                                  func(self.world, self.position, self.directions[i][0], self.directions[i][1]))


    def get_random_direction(self) -> Direction:
        directions: [Direction] = list(map(lambda pair : pair[0], self.directions))
        weights: [float] = list(map(lambda pair : pair[1], self.directions))
        probabilities: [float]
        if sum(weights) != 0:
            probabilities = list(map(lambda w : w/(sum(weights)), weights))
        else:
            probabilities = [1/len(directions)] * len(directions)
        return random.choice(array(directions), p=array(probabilities))
########################################################################################################################