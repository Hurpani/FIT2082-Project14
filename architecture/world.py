##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################
if TYPE_CHECKING:
    from architecture.actor import Actor

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
        self.__running: bool = False
        self.__delay: float = delay

        self.__width: int = width
        self.__height: int = height
        self.__scale: float = scale
        self.__world: [[Location]] = []
        for i in range(width):
            self.__world.append([None] * height)


    def set_location(self, location: Location, x: int, y: int):
        """\
    Set a grid location in this world to the specified Location instance.
        """
        if 0 <= x < self.__width and 0 <= y < self.__height:
            self.__world[x][y] = location
        else:
            raise InvalidLocationException()


    def add_actor(self, actor: Actor, x: int, y: int):
        if self.get_location(x, y).is_free():
            self.get_location(x, y).set_actor(actor)
        else:
            raise InvalidLocationException()


    def get_location(self, x: int, y: int):
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__world[x][y]
        else:
            raise InvalidLocationException()


    def run(self):
        self.__running = True
        while self.__running:
            for x in range(self.__width):
                for y in range(self.__height):
                    self.__world[x][y].tick(self, self.__delay, Position(x, y))


    def get_scale(self) -> float:
        return self.__scale


    def get_dimensions(self) -> (int, int):
        return self.__width, self.__height


    def get_printable(self) -> [[Colour]]:
        colours: [[Colour]] = []

        for j in range(self.__width):
            colours.append([None] * self.__height)

        for i in range(self.__width):
            for j in range(self.__height):
                colours[i][j] = self.get_location(i, j).get_colour()

        return colours
