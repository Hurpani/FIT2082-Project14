##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

if TYPE_CHECKING:
    from architecture.actor import Actor
    from architecture.object import Object
    from architecture.kinds import Kind

from architecture.exceptions.invalid_location import InvalidLocationException
from architecture.world_state import WorldState
from architecture.location import Location
from architecture.position import Position
from architecture.rendering.colour import Colour

class World:
    """\
The Map class. Manages a piece of terrain for the simulation.
    """

    DEFAULT_ITERATIONS: int = 100

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


    def add_object(self, object: Object, x: int, y: int):
        if (self.get_location(x, y) is not None):
            self.get_location(x, y).add_object(object)
        else:
            raise InvalidLocationException()


    def get_location(self, x: int, y: int) -> Location:
        if 0 <= x < self.__width and 0 <= y < self.__height:
            return self.__world[x][y]
        else:
            raise InvalidLocationException()


    def get_adjacent_locations(self, x: int, y: int, r: int = 1, require_free: bool = True) -> [Location]:
        """\
    Returns the locations with a Manhattan distance at most r from x,y.
        """
        locations: [Location] = []
        for i in range(max(x - r, 0), min(x + r + 1, self.__width - 1), 1):
            for j in range(max(y - r, 0), min(y + r + 1, self.__height - 1), 1):
                if abs(x - i) + abs(y - j) <= r and ((not require_free) or self.get_location(i, j).is_free()):
                    locations.append(self.get_location(i, j))
        return  locations


    def run(self, iterations: int = DEFAULT_ITERATIONS):
        self.__running = True
        count: int = 0
        # TODO : Make this nicer?
        while self.__running and count < iterations:
            actors: [(Actor, Location, Position)] = []
            for x in range(self.__width):
                for y in range(self.__height):
                    _updatable: (Actor, Location, Position) = self.__world[x][y].tick(self, self.__delay, Position(x, y))
                    if _updatable[0] is not None:
                        actors.append(_updatable)
            for (actor, location, position) in actors:
                actor.tick(self, self.__delay, location, position)
            count += 1


    def get_scale(self) -> float:
        return self.__scale


    def get_dimensions(self) -> (int, int):
        return self.__width, self.__height


    def get_max_objects_in_location(self, *kinds: [Kind]) -> int:
        c: int = 0
        for lst in self.__world:
            for loc in lst:
                t: int = len(loc.get_objects(*kinds)) if len(kinds) > 0 else len(loc.get_objects(*kinds))
                if t > c:
                    c = t
        return c


    def get_printable(self, *object_kinds: [Kind]) -> [[Colour]]:
        colours: [[Colour]] = []
        world_state: WorldState = WorldState(self.get_max_objects_in_location(*object_kinds))

        for j in range(self.__width):
            colours.append([None] * self.__height)

        for i in range(self.__width):
            for j in range(self.__height):
                colours[i][j] = self.get_location(i, j).get_colour(world_state, *object_kinds)

        return colours
