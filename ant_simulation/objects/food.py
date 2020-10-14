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


class Food(Object):
    ID: str = "food"

    @staticmethod
    def get_id() -> str:
        return Food.ID

    @staticmethod
    def create(kinds: [Kind] = []):
        return Food(kinds)

    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass

    def __init__(self, kinds: [Kind] = []):
        super().__init__(kinds)
        self.kinds.append(Kind.FOOD)
