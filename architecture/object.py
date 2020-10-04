from abc import ABC, abstractmethod

from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.world import World
from architecture.writeable import Writeable


class Object(Writeable):
    """\
An object that actors can interact with, which is participating
in the simulation.
    """
    @staticmethod
    def get_id() -> str:
        pass


    @staticmethod
    def create(kinds: [Kind] = []):
        pass

    def get_writeout_string(self, x: int, y: int) -> str:
        return f"{self.get_id()} {x} {y}"

    def add_kind(self, kind: Kind):
        self.kinds.append(kind)

    @abstractmethod
    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def __init__(self, kinds: [Kind] = []):
        self.kinds = kinds
