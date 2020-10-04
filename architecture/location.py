##############################
from __future__ import annotations
from typing import TYPE_CHECKING, Union
##############################

from abc import ABC
import random
from architecture.exceptions.invalid_location import InvalidLocationException
from architecture.rendering.colour import Colour

if TYPE_CHECKING:
    from architecture.actor import Actor
    from architecture.ground import Ground
    from architecture.object import Object
    from architecture.world import World
    from architecture.kinds import Kind
    from architecture.position import Position
    from architecture.world_state import WorldState


class Location(ABC):
    """\
The Location class. Manages a location in a map.
    """

    DEFAULT_OBJECTS_BASE_COLOUR: Colour = Colour(1, 0, 0)
    MIN_COLOUR_VAL: int = 50
    PHEROMONE_DETERIORATION_CHANCE: float = 0.05
    COMPLEX_PHEROMONE_DETERIORATION_CHANCE: float = 0.015
    PHEROMONE_COUNT_CAP: int = 20;
    PHEROMONE_COLOUR: Colour = Colour(90, 127, 0)

    def __init__(self, ground: Ground):
        self.ground: Ground = ground     # 1..1
        self.actor: Union[Actor, None] = None         # 0..1
        self.objects: [Object] = []      # 0..*
        # General ant pheromones:
        self.pheromones: int = 0
        # More complex pheromones:
            # For carrying food.
        self.foraging_pheromones: int = 0
            # For staying near the nest.
        self.brood_pheromones: int = 0


    def add_pheromones(self, num: int):
        if self.pheromones < Location.PHEROMONE_COUNT_CAP:
            self.pheromones += num


    def get_pheromone_count(self):
        return self.pheromones


    def add_foraging_pheromones(self, num: int):
        if self.foraging_pheromones < Location.PHEROMONE_COUNT_CAP:
            self.foraging_pheromones += num


    def get_foraging_pheromone_count(self):
        return self.foraging_pheromones


    def add_brood_pheromones(self, num: int):
        if self.brood_pheromones < Location.PHEROMONE_COUNT_CAP:
            self.brood_pheromones += num


    def get_brood_pheromone_count(self):
        return self.brood_pheromones


    def get_pheromone_colour(self) -> Colour:
        return Location.PHEROMONE_COLOUR.get_alt_blue(int(Colour.MAX_VALUE * (float(self.get_pheromone_count()) /
                                                                              Location.PHEROMONE_COUNT_CAP))).\
                                get_alt_red(int(Colour.MAX_VALUE * (float(self.get_foraging_pheromone_count()) /
                                                                              Location.PHEROMONE_COUNT_CAP)))

    def tick(self, world: World, elapsed: float, position: Position) -> (Actor, Location, Position):
        for obj in self.objects:
            obj.tick(world, elapsed, self, position)
        if self.get_ground().is_passable():
            # TODO: Fix this to be in terms of elapsed time (eg. with binomial distribution for probability).
            if random.random() < Location.PHEROMONE_DETERIORATION_CHANCE and self.pheromones > 0:
                self.pheromones -= 1
            if random.random() < Location.COMPLEX_PHEROMONE_DETERIORATION_CHANCE and self.foraging_pheromones > 0:
                self.foraging_pheromones -= 1
            if random.random() < Location.COMPLEX_PHEROMONE_DETERIORATION_CHANCE and self.brood_pheromones > 0:
                self.brood_pheromones -= 1
        return self.actor, self, position


    def get_objects_colour(self, world_state: WorldState) -> Colour:
        return Location.DEFAULT_OBJECTS_BASE_COLOUR.multiply((
            float(len(self.objects))/world_state.
                get_max_objects_in_location_count() if world_state.
                    get_max_objects_in_location_count() != 0 else 1) * Colour.MAX_VALUE).\
            get_alt_blue(Location.MIN_COLOUR_VAL)


    def get_colour(self, world_state: WorldState, *object_kinds: [Kind]) -> Colour:
        if self.actor is not None:
            return self.actor.get_colour()
        elif len(object_kinds) == 0 and self.get_pheromone_count() > 0:
            return self.get_pheromone_colour()
        elif len(self.get_objects(*object_kinds)) > 0:
            return self.get_objects_colour(world_state)
        else:
            return self.ground.get_colour()


    def set_actor(self, actor: Actor):
        if self.get_actor() is not None:
            raise InvalidLocationException()
        self.actor = actor


    def add_object(self, object: Object):
        self.objects.append(object)


    def remove_object(self, obj: Object):
        """\
    Removes the specified Object from this Location.
        """
        self.objects.remove(obj)


    def get_object_by_kind(self, kind: Kind):
        """\
    Returns a list of objects in this location which have the
        specified kind.
        """
        return self.get_objects(kind)
        # ret_list: [Object] = []
        # for obj in self.objects:
        #     if kind in obj.get_kinds():
        #         ret_list.append(obj)
        # return ret_list


    def get_actor(self) -> Union[Actor, None]:
        """\
    Returns the actor at this location.
        """
        return self.actor


    def remove_actor(self) -> Actor:
        """\
    Removes the actor at this location, and returns it.
        """
        actor: Actor = self.actor
        self.actor = None
        return actor


    def get_ground(self) -> Ground:
        """\
    Returns the ground of this location.
        """
        return self.ground


    @staticmethod
    def __any_in(of, lst):
        for x in of:
            if x in lst:
                return True
        return False

    def get_objects(self, *with_kinds: [Kind]) -> [Object]:
        """\
    Returns the objects stored at this location.
        """
        if len(with_kinds) == 0:
            return self.objects
        else:
            return list(filter(lambda k : self.__any_in(k.get_kinds(), with_kinds), self.objects))


    def is_free(self) -> bool:
        """\
    Return whether or not an actor can enter this location.
        """
        return self.ground.is_passable() and self.actor is None
