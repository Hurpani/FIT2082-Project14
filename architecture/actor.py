##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

from abc import ABC, abstractmethod
from architecture.kinds import Kind
from architecture.position import Position

if TYPE_CHECKING:
    from architecture.location import Location
    from architecture.world import World


class Actor(ABC):
    """\
An moving, reacting object participating in the simulation.
    """

    @staticmethod
    def create(pos: Position = Position(), kinds: [Kind] = []):
        pass

    @staticmethod
    def get_id() -> str:
        pass

    @abstractmethod
    def tick(self, world: World, elapsed: float, location: Location):
        pass

    @abstractmethod
    def add_kind(self, kind: Kind):
        pass

    def get_kinds(self) -> [Kind]:
        return []
