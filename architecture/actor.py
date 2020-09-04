from abc import ABC, abstractmethod

from architecture.kinds import Kind
from architecture.world import World


class Actor(ABC):
    """\
An moving, reacting object participating in the simulation.
    """
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def tick(self, elapsed: float, world: World):
        pass

    def get_kinds(self) -> [Kind]:
        return []

    def __init__(self):
        pass
