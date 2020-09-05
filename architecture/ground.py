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

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def is_passable(self) -> bool:
        pass

    def get_kinds(self) -> [Kind]:
        return []

    def __init__(self):
        pass