##############################
from __future__ import annotations
from typing import TYPE_CHECKING
##############################

from abc import abstractmethod

from architecture.attributes import Attributes
from architecture.kinds import Kind
from architecture.position import Position
from architecture.rendering.renderable import Renderable

if TYPE_CHECKING:
    from architecture.location import Location
    from architecture.world import World


class Actor(Renderable):
    """\
A moving, reacting object participating in the simulation.
    """

    @staticmethod
    def create(attributes: Attributes = None, kinds: [Kind] = []) -> Actor:
        pass


    @staticmethod
    def get_id() -> str:
        pass


    @abstractmethod
    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass


    def get_writeout_string(self, x: int, y: int) -> str:
        return f"{self.get_id()} {x} {y} {self.get_attributes_string()}"


    def get_attributes_string(self) -> str:
        return ""


    def add_kind(self, kind: Kind):
        self.kinds.append(kind)


    def get_kinds(self) -> [Kind]:
        return self.kinds


    def __init__(self, kinds: [Kind] = []):
        self.kinds = kinds
