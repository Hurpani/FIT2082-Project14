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


class Location(ABC):
    """\
The Location class. Manages a location in a map.
    """

    DEFAULT_OBJECTS_COLOUR: Colour = Colour(0, 0, 0)

    def __init__(self, ground: Ground):
        self.ground: Ground = ground     # 1..1
        self.actor: Actor = None         # 0..1
        self.objects: [Object] = []      # 0..*


    def tick(self, world: World, elapsed: float):
        self.actor.tick(world, elapsed, self)
        for obj in self.objects:
            obj.tick(world, elapsed, self)


    def get_objects_colour(self) -> Colour:
        return Location.DEFAULT_OBJECTS_COLOUR


    def get_colour(self) -> Colour:
        if self.actor is not None:
            return self.actor.get_colour()
        elif len(self.objects) > 0:
            return self.get_objects_colour()
        else:
            return self.ground.get_colour()


    def set_actor(self, actor: Actor):
        if self.get_actor() is not None:
            raise InvalidLocationException()
        self.actor = actor


    def add_object(self, object: Object):
        self.objects.append(object)


    def get_object_by_kind(self, kind: Kind):
        """\
    Returns a list of objects in this location which have the
        specified kind.
        """
        ret_list: [Object] = []
        for obj in self.objects:
            if kind in obj.get_kinds():
                ret_list.append(obj)
        return ret_list


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


    def get_objects(self) -> [Object]:
        """\
    Returns the objects stored at this location.
        """
        return self.objects


    def is_free(self) -> bool:
        """\
    Return whether or not an actor can enter this location.
        """
        return self.ground.is_passable()# and self.actor is None
