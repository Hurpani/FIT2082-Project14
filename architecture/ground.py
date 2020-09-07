from abc import ABC, abstractmethod
from architecture.kinds import Kind
from architecture.position import Position


class Ground(ABC):
    """\
A piece of ground participating in the simulation.
    """

    @staticmethod
    def create(pos: Position = Position(), kinds: [Kind] = []):
        pass

    @staticmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def is_passable(self) -> bool:
        pass

    @abstractmethod
    def add_kind(self, kind: Kind):
        pass

    def get_kinds(self) -> [Kind]:
        return []
