##############################
from __future__ import annotations

import math
from typing import Callable, Dict, List, Tuple
##############################
from architecture.exceptions.invalid_location import InvalidLocationException

from numpy import random, array
from architecture.world import World
from architecture.location import Location
from architecture.position import Position

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

    def reversed(self) -> Direction:
        return Direction(-1 * self.x, -1 * self.y)

    def dot(self, other: Direction) -> float:
        return (self.x * other.x) + (self.y * other.y)

    @staticmethod
    def clamped_similarity(d1: Direction, d2: Direction) -> float:
        dotp: float = d1.dot(d2)
        return 1 if dotp > 0 else (0.5 if dotp == 0 else 0.01)

    def __sub__(self, other) -> Direction:
        return Direction(self.x - other.x, self.y - other.y)

    def size_l1(self) -> float:
        return abs(self.x) + abs(self.y)

    def size_l2(self) -> float:
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    # FIXME: These methods should be replaced and considered deprecated.
    @staticmethod
    def similarity_score(d1: Direction, d2: Direction) -> float:
        OFFSET: float = 1
        return 1/(OFFSET + Direction.dif_mag(d1, d2))

    @staticmethod
    def dif_mag(d1: Direction, d2: Direction) -> float:
        dif: (float, float) = (d1.get()[0] - d2.get()[0], d1.get()[1] - d2.get()[1])
        return math.sqrt((dif[0] * dif[0]) + (dif[1] * dif[1]))


class Directions:
    """\
The Directions class manages pairs of possible movement directions, and associated
    weights.
    """

    ####################################################################################################################
    # Space < Time
    ####################################################################################################################
    compiled_positions: Dict[World, Dict[(int, int), List[(Direction, float)]]] = {}

    @staticmethod
    def get_weighted_directions(world: World, x: int, y: int) -> [(Direction, float)]:
        directions: [(Directions, float)] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j:
                    continue
                weight: float
                try:
                    loc: Location = world.get_location(x + i, y + j)
                    weight = 1 if loc.is_free() else 0
                except (IndexError, InvalidLocationException):
                    weight = 0
                directions.append((Direction(i, j), weight))
        return directions

    @staticmethod
    def get_baked(world: World, position: Position) -> [(Direction, float)]:
        if world not in Directions.compiled_positions:
            Directions.compiled_positions[world] = {}
            for i in range(world.get_dimensions()[0]):
                for j in range(world.get_dimensions()[1]):
                    Directions.compiled_positions[world][(i, j)] = Directions.get_weighted_directions(world, i, j)
        return Directions.compiled_positions[world][(position.x, position.y)].copy()
    ####################################################################################################################



    def __init__(self, world: World, position: Position, use_baked_data: bool = True):
        self.world: World = world
        self.position: Position = position
        self.directions: [(Direction, float)] = []
        if use_baked_data:
            self.directions = Directions.get_baked(world, position)
        else:
            self.directions = Directions.get_weighted_directions(world, position.x, position.y)


    def bias_seq(self, *funcs: Callable[[World, Position, Direction, float], float]):
        for f in funcs:
            self.bias(f)


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