from abc import ABC
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from architecture.actor import Actor
    from architecture.ground import Ground
    from architecture.object import Object
    from architecture.world import World


class Location(ABC):
    """\
The Location class. Manages a location in a map.
    """

    def __init__(self):#, world: World):
        self.world: World = None       # 1..1
        self.ground: Ground = None      # 1..1
        self.actor: Actor = None        # 0..1
        self.objects: [Object] = []     # 0..*

    def get_actor(self) -> Actor:
        """\
    Returns the actor at this location.
        """
        return self.actor

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
