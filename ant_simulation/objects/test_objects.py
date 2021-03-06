##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

from architecture.object import Object
from architecture.kinds import Kind

if TYPE_CHECKING:
    from architecture.location import Location
    from architecture.position import Position
    from architecture.world import World



class TestObject(Object):
    @staticmethod
    def get_id() -> str:
        return "test_object"

    @staticmethod
    def create(kinds: [Kind] = []):
        return TestObject(kinds)

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass

    def __init__(self, kinds: [Kind] = []):
        super().__init__(kinds)
        self.kinds.append(Kind.TRACKER)
