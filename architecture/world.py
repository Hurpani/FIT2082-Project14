##############################
from __future__ import annotations

from typing import TYPE_CHECKING, Union

##############################

if TYPE_CHECKING:
    from architecture.actor import Actor
    from architecture.object import Object
    from architecture.kinds import Kind

from pathlib import Path
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
    WRITE_OUT_FILE_PATH = Path("saves/")
    WRITE_OUT_ACTORS_FILE_NAME: str = "world_save.txt"
    WRITE_OUT_OBJECTS_FILE_NAME: str = "world_objects.txt"
    WRITE_OUT_PHEROMONES_FILE_NAME: str = "pheromones_save.txt"

    def __init__(self, width: int, height: int, scale: float = 1.0, delay: float = 1.0,
                 bias_test_scale: float = 1.0, bias_test_pheromones_scale: float = 1.0):
        """\
    Constructor for the world class. Accepts a scale as an argument, which informs locations of
        their real-world dimensions.

        @:param width: the number of tiles across of this World.
        @:param height: the number of tiles vertically of this World.
        @:param scale: the real-world dimensions of this World.
        """
        self.__delay: float = delay

        self.__width: int = width
        self.__height: int = height
        self.__scale: float = scale
        self.__world: [[Location]] = []
        self.__bias_test_scale: float = bias_test_scale
        self.__bias_test_pheromones_scale: float = bias_test_pheromones_scale
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


    def set_testing_scale(self, scale: float) -> None:
        self.__bias_test_scale = scale


    def set_pheromone_testing_scale(self, scale: float) -> None:
        self.__bias_test_pheromones_scale = scale


    def get_pheromone_testing_scale(self) -> float:
        """\
    The pheromone testing scale of the world indicates how distinct agent decision-making should
        be from random decision-making. A scale of zero should denote no non-random decision-making,
        and a scale of 1.0 should correspond to default behaviour. The behaviours we are concerned
        with controlling via this scale are those associated with pheromone biasing.
        """
        return self.__bias_test_pheromones_scale


    def get_testing_scale(self) -> float:
        """\
    The testing scale of the world indicates how distinct agent decision-making should be from
        random decision-making. A scale of zero should denote no non-random decision-making,
        and a scale of 1.0 should correspond to default behaviour. The behaviours we are concerned
        with controlling via this scale are those associated with an ant's general behaviour, such
        as seeking out food or path-finding in roughly-straight lines.
        """
        return self.__bias_test_scale


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


    def get_adjacent_locations_with_positions(self, x: int, y: int, r: int = 1, require_free: bool = True) -> [Location]:
        """\
    Returns the locations with a Manhattan distance at most r from x,y.
        """
        locations: [(Location, int, int)] = []
        for i in range(max(x - r, 0), min(x + r + 1, self.__width - 1), 1):
            for j in range(max(y - r, 0), min(y + r + 1, self.__height - 1), 1):
                if abs(x - i) + abs(y - j) <= r and ((not require_free) or self.get_location(i, j).is_free()):
                    locations.append((self.get_location(i, j), i, j))
        return  locations


    def run(self, iterations: int = DEFAULT_ITERATIONS):
        for i in range(iterations):
            actors: [(Actor, Location, Position)] = []
            for x in range(self.__width):
                for y in range(self.__height):
                    _updatable: (Actor, Location, Position) = self.__world[x][y].tick(self, self.__delay, Position(x, y))
                    if _updatable[0] is not None:
                        actors.append(_updatable)
            for (actor, location, position) in actors:
                actor.tick(self, self.__delay, location, position)


    def restore_pheromones(self):
        with open((World.WRITE_OUT_FILE_PATH / World.WRITE_OUT_PHEROMONES_FILE_NAME), "r") as file:
            for line in file.readlines():
                x, y = line.split()[0], line.split()[1]
                p, fp, bp = int(line.split()[2]), int(line.split()[3]), int(line.split()[4])
                loc: Location = self.get_location(int(x), int(y))
                loc.pheromones, loc.foraging_pheromones, loc.brood_pheromones = p, fp, bp


    def write_out(self):
        """\
    Takes a snapshot of as much of the state of actors in this world as possible, and the pheromone counts.
        """
        with open((World.WRITE_OUT_FILE_PATH / World.WRITE_OUT_ACTORS_FILE_NAME), "w+") as file:
            for x in range(self.__width):
                for y in range(self.__height):
                    actor: Union[Actor, None] = self.get_location(x, y).get_actor()
                    if actor is not None:
                        file.write(actor.get_writeout_string(x, y) + "\n")
        with open((World.WRITE_OUT_FILE_PATH / World.WRITE_OUT_OBJECTS_FILE_NAME), "w+") as file:
            for x in range(self.__width):
                for y in range(self.__height):
                    for obj in self.get_location(x, y).get_objects():
                        file.write(obj.get_writeout_string(x, y) + "\n")
        with open((World.WRITE_OUT_FILE_PATH / World.WRITE_OUT_PHEROMONES_FILE_NAME), "w+") as file:
            for x in range(self.__width):
                for y in range(self.__height):
                    file.write(f"{x} {y} {self.get_location(x, y).get_pheromone_count()} \
{self.get_location(x, y).get_foraging_pheromone_count()} {self.get_location(x, y).get_brood_pheromone_count()}\n")


    @staticmethod
    def move(frm: Location, to: Location):
        if to.is_free():
            to.set_actor(frm.get_actor())
            frm.remove_actor()


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
