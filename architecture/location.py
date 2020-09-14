##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

from abc import ABC
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

    def __init__(self, ground: Ground):
        self.ground: Ground = ground     # 1..1
        self.actor: Actor = None         # 0..1
        self.objects: [Object] = []      # 0..*


    def tick(self, world: World, elapsed: float, position: Position) -> (Actor, Location, Position):
        for obj in self.objects:
            obj.tick(world, elapsed, self, position)
        return self.actor, self, position


    def get_objects_colour(self, world_state: WorldState) -> Colour:
        return Location.DEFAULT_OBJECTS_BASE_COLOUR.multiply((float(len(self.objects))/world_state.get_max_objects_in_location_count() if world_state.get_max_objects_in_location_count() != 0 else 1) * Colour.MAX_VALUE).\
            get_alt_blue(Location.MIN_COLOUR_VAL)


    def get_colour(self, world_state: WorldState, *object_kinds: [Kind]) -> Colour:
        if self.actor is not None:
            return self.actor.get_colour()
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


    def get_actor(self) -> Actor:
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
