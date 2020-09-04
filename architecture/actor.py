from abc import ABC, abstractmethod
from architecture.kinds import Kind
from architecture.position import Position
from architecture.world import World


class Actor(ABC):
    """\
An moving, reacting object participating in the simulation.
    """

    @staticmethod
    def create(pos: Position = Position()):
        pass

    @staticmethod
    def get_id() -> str:
        pass

    @abstractmethod
    def tick(self, elapsed: float, world: World):
        pass

    def get_kinds(self) -> [Kind]:
        return []
