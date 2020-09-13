from abc import ABC, abstractmethod

from architecture.kinds import Kind
from architecture.location import Location
from architecture.position import Position
from architecture.world import World


class Object(ABC):
    """\
An object that actors can interact with, which is participating
in the simulation.
    """
    @staticmethod
    def get_id(self) -> str:
        pass


    @staticmethod
    def create(kinds: [Kind] = []):
        pass

    @abstractmethod
    def add_kind(self, kind: Kind):
        pass

    @abstractmethod
    def tick(self, world: World, elapsed: float, location: Location, position: Position):
        pass

    def get_kinds(self) -> [Kind]:
        return self.kinds

    def __init__(self, kinds: [Kind] = []):
        self.kinds = kinds
