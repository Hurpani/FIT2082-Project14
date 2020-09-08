##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

from architecture.exceptions.invalid_location import InvalidLocationException
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour
from architecture.rendering.plotter import Plotter

class World:
    """\
The Map class. Manages a piece of terrain for the simulation.
    """

    def __init__(self, width: int, height: int, scale: float = 1.0, delay: float = 1.0):
        """\
    Constructor for the world class. Accepts a scale as an argument, which informs locations of
        their real-world dimensions.

        @:param width: the number of tiles across of this World.
        @:param height: the number of tiles vertically of this World.
        @:param scale: the real-world dimensions of this World.
        """
        self.running: bool = False
        self.delay: float = delay

        self.width: int = width
        self.height: int = height
        self.scale: float = scale
        self.world: [[Location]] = []
        for i in range(width):
            self.world.append([None] * height)


    def set_location(self, location: Location, x: int, y: int):
        """\
    Set a grid location in this world to the specified Location instance.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.world[x][y] = location
        else:
            raise InvalidLocationException()


    def get_location(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.world[x][y]
        else:
            raise InvalidLocationException()


    def run(self):
        self.running = True
        while self.running:
            for x in range(self.width):
                for y in range(self.height):
                    self.world[x][y].tick(self, self.delay, Position(x, y))


    def get_scale(self) -> float:
        return self.scale


    def get_printable(self) -> [[Colour]]:
        colours: [[Colour]] = []

        for j in range(self.width):
            colours.append([None] * self.height)

        for i in range(self.width):
            for j in range(self.height):
                colours[i][j] = self.get_location(i, j).get_colour()

        return colours
